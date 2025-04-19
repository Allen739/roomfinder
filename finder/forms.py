from django import forms
from finder.models import Room
from django.core.exceptions import ValidationError
import datetime


class RoomSearchForm(forms.Form):
    DAYS = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
    ]

    DURATIONS = [
        (30, "30 minutes"),
        (60, "1 hour"),
        (90, "1 hour 30 minutes"),
    ]

    building = forms.ChoiceField(label="Building")
    day = forms.ChoiceField(choices=DAYS, label="Day")
    time = forms.TimeField(
        label="Time",
        widget=forms.TimeInput(
            attrs={
                "type": "time"}))
    duration = forms.ChoiceField(choices=DURATIONS, label="Duration (minutes)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get unique buildings from Room model
        buildings = Room.objects.values('building').distinct()
        # Create choices: [("ALL", "All Buildings"), ("Science Block", "Science
        # Block"), ...]
        building_choices = [("ALL", "All Buildings")] + [
            (b["building"], b["building"]) for b in buildings
        ]
        # Handle case with no buildings
        if len(building_choices) == 1:  # Only "ALL"
            building_choices = [("ALL", "No buildings available")]
        self.fields["building"].choices = building_choices

    def clean(self):
        cleaned_data = super().clean()
        time = cleaned_data.get("time")
        duration = cleaned_data.get("duration")

        if time and duration:
            try:
                # Convert duration to integer
                duration = int(duration)
                # Calculate end time
                start_datetime = datetime.datetime.combine(
                    datetime.date.today(), time)
                end_datetime = start_datetime + \
                    datetime.timedelta(minutes=duration)
                end_time = end_datetime.time()

                # Check if end_time is too late (after 23:00)
                if end_time > datetime.time(23, 0):
                    raise ValidationError(
                        "The selected time and duration extend beyond 11:00 PM.")
                # Check if time is too early (before 07:00)
                if time < datetime.time(7, 0):
                    raise ValidationError(
                        "The selected time is before 7:00 AM.")
            except (ValueError, TypeError):
                raise ValidationError("Invalid time or duration format.")
        return cleaned_data


class ExcelUploadForm(forms.Form):
    rooms_file = forms.FileField(
        label="Rooms Excel File (rooms.xlsx)",
        required=False)
    timetable_file = forms.FileField(
        label="Timetable Excel File (timetable.xlsx)",
        required=False)

    def clean(self):
        cleaned_data = super().clean()
        rooms_file = cleaned_data.get("rooms_file")
        timetable_file = cleaned_data.get("timetable_file")
        if not rooms_file and not timetable_file:
            raise forms.ValidationError(
                "At least one file (rooms or timetable) must be uploaded.")
        return cleaned_data
