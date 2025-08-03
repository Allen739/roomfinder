import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone
from finder.models import Room, ClassSchedule
import re


class Command(BaseCommand):
    help = "Load timetable data from timetable.xlsx into ClassSchedule model."

    def handle(self, *args, **options):
        # Clear existing schedules (for testing)
        ClassSchedule.objects.all().delete()

        # Read Excel file
        try:
            df = pd.read_excel("sample_data/timetable.xlsx")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                "timetable.xlsx not found in project root."))
            return

        # Validate columns
        expected_columns = [
            "Course",
            "Subject",
            "Day/Time",
            "Room",
            "Building",
            "Lecturer"]
        if not all(col in df.columns for col in expected_columns):
            self.stdout.write(
                self.style.ERROR(
                    f"Excel file must have columns: {expected_columns}"))
            return

        # Validate days
        valid_days = {choice[0] for choice in ClassSchedule._meta.get_field(
            'day').choices}  # e.g., {"Mon", "Tue", ...}
        created_count = 0
        for _, row in df.iterrows():
            # Parse Day/Time (e.g., "Mon 08:00–09:30" or "Monday 8:00 AM-9:30
            # AM")
            day_time = str(row["Day/Time"]).strip()
            # Flexible regex: supports "Mon 08:00–09:30" or "Monday 8:00
            # AM-9:30 AM"
            match = re.match(
                r"(?P<day>\w+)\s+(?P<start>\d{1,2}:\d{2}\s*(?:AM|PM)?)[-–](?P<end>\d{1,2}:\d{2}\s*(?:AM|PM)?)",
                day_time)
            if not match:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping invalid Day/Time: {day_time}"))
                continue

            day, start_time_str, end_time_str = match.groups()
            # Map full day names to short (e.g., "Monday" → "Mon")
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
            day = day_map.get(day, None)
            if day not in valid_days:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping invalid day: {day}"))
                continue

            # Parse times (handle AM/PM or 24-hour)
            try:
                start_time = timezone.datetime.strptime(
                    start_time_str,
                    "%I:%M %p").time() if "AM" in start_time_str or "PM" in start_time_str else timezone.datetime.strptime(
                    start_time_str,
                    "%H:%M").time()
                end_time = timezone.datetime.strptime(
                    end_time_str,
                    "%I:%M %p").time() if "AM" in end_time_str or "PM" in end_time_str else timezone.datetime.strptime(
                    end_time_str,
                    "%H:%M").time()
            except ValueError:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping invalid time format: {day_time}"))
                continue

            # Find Room
            room_name = str(row["Room"]).strip()
            building = str(row["Building"]).strip()
            try:
                room = Room.objects.get(name=room_name, building=building)
            except Room.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping: Room {room_name} in {building} not found."))
                continue

            # Validate course, subject, lecturer
            course = str(row["Course"]).strip()[:50]
            subject = str(row["Subject"]).strip()[:100]
            lecturer = str(row["Lecturer"]).strip()[:100]
            if not course or not subject or not lecturer:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping: Missing course/subject/lecturer for {day_time}"))
                continue

            # Create ClassSchedule
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
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {created_count} timetable entries."))
