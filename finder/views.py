from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, ClassSchedule
from .forms import RoomSearchForm, ExcelUploadForm
from io import BytesIO
import pandas as pd
import re
from django.utils import timezone
import datetime
import logging

# Set up logging for debugging
logger = logging.getLogger(__name__)

def search_rooms(request):
    form = RoomSearchForm(request.POST or None)
    available_rooms = []
    unavailable_rooms = []
    errors = []
    search_time = None
    duration = None

    if request.method == "POST" and form.is_valid():
        building = form.cleaned_data["building"]
        day = form.cleaned_data["day"]
        search_time = form.cleaned_data.get("time")
        duration = form.cleaned_data.get("duration")

        room_queryset = Room.objects.all() if building == "ALL" else Room.objects.filter(building=building)
        rooms = room_queryset.prefetch_related('schedules')

        if not rooms.exists():
            errors.append(f"No rooms found for the selected criteria.")
        else:
            # First, build the full timeline data for every room
            all_rooms_with_timelines = []
            for room in rooms:
                schedules = room.schedules.filter(day=day, is_cancelled=False).order_by('start_time')
                timeline = []
                last_end_time = datetime.time(7, 0)

                for schedule in schedules:
                    if schedule.start_time > last_end_time:
                        timeline.append({"type": "free", "start": last_end_time, "end": schedule.start_time})
                    timeline.append({"type": "booked", "start": schedule.start_time, "end": schedule.end_time, "course": schedule.course})
                    last_end_time = schedule.end_time
                
                if last_end_time < datetime.time(23, 0):
                    timeline.append({"type": "free", "start": last_end_time, "end": datetime.time(23, 0)})
                
                all_rooms_with_timelines.append({"room": room, "timeline": timeline})

            # If a specific time is searched, sort rooms into available/unavailable lists
            if search_time and duration:
                search_start_time = search_time
                search_end_time = (datetime.datetime.combine(datetime.date.today(), search_start_time) + datetime.timedelta(minutes=duration)).time()

                for room_data in all_rooms_with_timelines:
                    is_available = False
                    for block in room_data["timeline"]:
                        if block["type"] == "free":
                            # Check if the search window fits entirely within this free block
                            if block["start"] <= search_start_time and block["end"] >= search_end_time:
                                is_available = True
                                break
                    if is_available:
                        available_rooms.append(room_data)
                    else:
                        unavailable_rooms.append(room_data)
            else:
                # If no specific time, all rooms are in the "unavailable" list for display purposes
                unavailable_rooms = all_rooms_with_timelines

    # Convert datetime objects to strings for template rendering
    for room_list in [available_rooms, unavailable_rooms]:
        for room_data in room_list:
            for block in room_data["timeline"]:
                block['start_str'] = block['start'].strftime("%H:%M")
                block['end_str'] = block['end'].strftime("%H:%M")
                total_duration = (datetime.datetime.combine(datetime.date.min, datetime.time(23,0)) - datetime.datetime.combine(datetime.date.min, datetime.time(7,0))).total_seconds()
                block['start_percentage'] = ((datetime.datetime.combine(datetime.date.min, block['start']) - datetime.datetime.combine(datetime.date.min, datetime.time(7,0))).total_seconds() / total_duration) * 100
                block['width_percentage'] = ((datetime.datetime.combine(datetime.date.min, block['end']) - datetime.datetime.combine(datetime.date.min, block['start'])).total_seconds() / total_duration) * 100

    context = {
        "form": form,
        "available_rooms": available_rooms,
        "unavailable_rooms": unavailable_rooms,
        "errors": errors,
        "search_performed": search_time and duration
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, "finder/timeline_partial.html", context)

    return render(request, "finder/search.html", context)

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

def home(request):
    return redirect("finder:search_rooms")