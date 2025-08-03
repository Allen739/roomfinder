from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, ClassSchedule
from .forms import RoomSearchForm
from .forms import ExcelUploadForm
from io import BytesIO
import pandas as pd
import re
from django.utils import timezone
import datetime
import logging

# Set up logging for debugging
logger = logging.getLogger(__name__)


def search_rooms(request):
    form = RoomSearchForm()
    free_rooms = []
    errors = []

    if request.method == "POST":
        form = RoomSearchForm(request.POST)
        if form.is_valid():
            building = form.cleaned_data["building"]
            day = form.cleaned_data["day"]
            time = form.cleaned_data["time"]
            duration = int(form.cleaned_data["duration"])

            # Log the input for debugging
            logger.debug(
                f"Search: building={building}, day={day}, time={time}, duration={duration}")

            # Calculate time range with 10-minute buffer
            start_datetime = timezone.datetime.combine(timezone.now(), time)
            end_datetime = start_datetime + \
                datetime.timedelta(minutes=duration)
            start_time = start_datetime.time()
            end_time = end_datetime.time()

            # Double-check time range (fallback)
            if end_time > datetime.time(23, 0) or start_time < datetime.time(7, 0):
                errors.append(
                    "The selected time and duration are outside allowed "
                    "hours (7:00 AM–11:00 PM).")
                logger.warning(
                    f"Invalid time range: start={start_time}, end={end_time}")
            else:
                buffer_end_time = (end_datetime +
                                   datetime.timedelta(minutes=10)).time()

                # Get rooms based on building
            if building == "ALL":
                all_rooms = Room.objects.all()
            else:
                all_rooms = Room.objects.filter(building__iexact=building)

            if not all_rooms.exists():
                errors.append("No rooms found for the selected building.")
            else:

                # Find booked rooms (not canceled) during the time range +
                # buffer
                booked_rooms = Room.objects.filter(
                    schedules__day=day,
                    schedules__start_time__lte=buffer_end_time,
                    schedules__end_time__gt=start_time,
                    schedules__is_cancelled=False
                ).distinct()

                # Free rooms = all rooms - booked rooms
                free_rooms = all_rooms.exclude(id__in=booked_rooms)

                if not free_rooms:
                    building_label = ("any building" if not building 
                                      else f"Building {building}")
                    errors.append(
                        f"No rooms available in {building_label} on {day} "
                        f"at {time} for {duration} minutes.")

        else:
            # Log form errors and add to errors list
            logger.error(f"Form validation failed: {form.errors}")
            for field, error_list in form.errors.items():
                if field == "__all__":
                    # Non-field errors (e.g., from clean())
                    errors.extend(error_list)
                else:
                    errors.extend(
                        [f"{field.capitalize()}: {error}" for error in error_list])

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, "finder/search.html#results-container", {
            "free_rooms": free_rooms,
            "errors": errors,
        })
    
    return render(request, "finder/search.html", {
        "form": form,
        "free_rooms": free_rooms,
        "errors": errors,
    })


# ... (other imports and code unchanged)
@staff_member_required
def upload_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            rooms_file = form.cleaned_data["rooms_file"]
            timetable_file = form.cleaned_data["timetable_file"]

            # Process rooms file (unchanged)
            rooms_count = 0
            if rooms_file:
                try:
                    df = pd.read_excel(BytesIO(rooms_file.read()))
                    expected_columns = ["Room", "Building"]
                    if not all(col in df.columns for col in expected_columns):
                        messages.error(
                            request, f"Rooms file must have columns: {expected_columns}")
                    else:
                        Room.objects.all().delete()  # Clear for testing
                        for _, row in df.iterrows():
                            room_name = str(row["Room"]).strip()
                            building = str(row["Building"]).strip()
                            if room_name and building:
                                Room.objects.update_or_create(
                                    name=room_name, building=building, defaults={
                                        "name": room_name, "building": building})
                                rooms_count += 1
                        messages.success(
                            request, f"Loaded {rooms_count} rooms.")
                except Exception as e:
                    messages.error(request,
                                   f"Error processing rooms file: {str(e)}")

            # Process timetable file
            timetable_count = 0
            if timetable_file:
                try:
                    df = pd.read_excel(BytesIO(timetable_file.read()))
                    expected_columns = [
                        "Course",
                        "Subject",
                        "Day/Time",
                        "Room",
                        "Building",
                        "Lecturer"]
                    if not all(col in df.columns for col in expected_columns):
                        messages.error(
                            request, f"Timetable file must have columns: {expected_columns}")
                    else:
                        ClassSchedule.objects.all().delete()  # Clear for testing
                        valid_days = {choice[0]
                                      for choice in ClassSchedule.DAY_CHOICES}
                        day_map = {
                            "Monday": "Mon",
                            "Tuesday": "Tue",
                            "Wednesday": "Wed",
                            "Thursday": "Thu",
                            "Friday": "Fri",
                            "Mon": "Mon",
                            "Tue": "Tue",
                            "Wed": "Wed",
                            "Thu": "Thu",
                            "Fri": "Fri"}
                        for index, row in df.iterrows():
                            day_time = str(row["Day/Time"]).strip()
                            # Log row data for debugging

                            match = re.match(
                                r"(?P<day>\w+)\s+(?P<start>\d{1,2}:\d{2}\s*"
                                r"(?:AM|PM)?)[-–](?P<end>\d{1,2}:\d{2}\s*"
                                r"(?:AM|PM)?)",
                                day_time)
                            if not match:
                                messages.warning(
                                    request, 
                                    f"Row {index}: Skipped due to invalid "
                                    f"Day/Time: {day_time}")
                                continue
                            day, start_time_str, end_time_str = match.groups()
                            day = day_map.get(day, None)
                            if day not in valid_days:
                                messages.warning(
                                    request, 
                                    f"Row {index}: Skipped due to invalid "
                                    f"day: {day}")
                                continue
                            try:
                                if ("AM" in start_time_str or 
                                    "PM" in start_time_str):
                                    start_time = timezone.datetime.strptime(
                                        start_time_str, "%I:%M %p").time()
                                else:
                                    start_time = timezone.datetime.strptime(
                                        start_time_str, "%H:%M").time()
                                
                                if ("AM" in end_time_str or 
                                    "PM" in end_time_str):
                                    end_time = timezone.datetime.strptime(
                                        end_time_str, "%I:%M %p").time()
                                else:
                                    end_time = timezone.datetime.strptime(
                                        end_time_str, "%H:%M").time()
                            except ValueError as e:
                                messages.warning(
                                    request,
                                    f"Row {index}: Skipped due to invalid "
                                    f"time format: {day_time} ({str(e)})")
                                continue
                            room_name = str(row["Room"]).strip()
                            building = str(row["Building"]).strip()
                            try:
                                room = Room.objects.get(
                                    name=room_name, building=building)
                            except Room.DoesNotExist:
                                messages.warning(
                                    request, f"Row {index}: Skipped: Room {room_name} in {building} not found.")
                                continue
                            course = str(row["Course"]).strip()[:50]
                            subject = str(row["Subject"]).strip()[:100]
                            lecturer = str(row["Lecturer"]).strip()[:100]
                            if not course or not subject or not lecturer:
                                messages.warning(
                                    request,
                                    f"Row {index}: Skipped: Missing "
                                    f"course/subject/lecturer: "
                                    f"Course={course}, Subject={subject}, "
                                    f"Lecturer={lecturer}")
                                continue
                            ClassSchedule.objects.create(
                                course=course,
                                subject=subject,
                                day=day,
                                start_time=start_time,
                                end_time=end_time,
                                room=room,
                                lecturer=lecturer,
                                is_cancelled=False,
                            )
                            timetable_count += 1
                        messages.success(
                            request, f"Loaded {timetable_count} timetable entries.")
                        return redirect("finder:search_rooms")
                except Exception as e:
                    messages.error(
                        request,
                        f"Error processing timetable file: {str(e)}")

    else:
        form = ExcelUploadForm()

    return render(request, "finder/upload_excel.html", {"form": form})
