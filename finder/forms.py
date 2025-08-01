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
        (120, "2 hours"),
    ]

    building = forms.ChoiceField(
        label="Building",
        help_text="Select a specific building or search all buildings",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_building'
        })
    )
    day = forms.ChoiceField(
        choices=DAYS, 
        label="Day",
        help_text="Select the day of the week",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_day'
        })
    )
    time = forms.TimeField(
        label="Start Time",
        help_text="Enter your preferred start time (7:00 AM - 11:00 PM)",
        widget=forms.TimeInput(attrs={
            "type": "time",
            'class': 'form-control',
            'min': '07:00',
            'max': '23:00',
            'id': 'id_time'
        })
    )
    duration = forms.ChoiceField(
        choices=DURATIONS, 
        label="Duration",
        help_text="How long do you need the room?",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_duration'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get unique buildings from Room model
        buildings = Room.objects.values('building').distinct().order_by('building')
        # Create choices: [("ALL", "All Buildings"), ("Science Block", "Science Block"), ...]
        building_choices = [("ALL", "All Buildings")] + [
            (b["building"], b["building"]) for b in buildings
        ]
        # Handle case with no buildings
        if len(building_choices) == 1:  # Only "ALL"
            building_choices = [("ALL", "No buildings available")]
        self.fields["building"].choices = building_choices

    def clean_time(self):
        time = self.cleaned_data.get('time')
        if time:
            if time < datetime.time(7, 0):
                raise ValidationError("Start time cannot be before 7:00 AM.")
            if time > datetime.time(23, 0):
                raise ValidationError("Start time cannot be after 11:00 PM.")
        return time

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
                        "The selected time and duration extend beyond 11:00 PM. "
                        "Please choose an earlier time or shorter duration.")
                        
                # Store calculated end time for use in view
                cleaned_data['calculated_end_time'] = end_time
                
            except (ValueError, TypeError):
                raise ValidationError("Invalid time or duration format.")
        return cleaned_data


class ExcelUploadForm(forms.Form):
    rooms_file = forms.FileField(
        label="Rooms Excel File",
        required=False,
        help_text="Upload an Excel file (.xlsx) with Room and Building columns",
        widget=forms.FileInput(attrs={
            'accept': '.xlsx,.xls',
            'class': 'form-control-file'
        })
    )
    timetable_file = forms.FileField(
        label="Timetable Excel File",
        required=False,
        help_text="Upload an Excel file (.xlsx) with Course, Subject, Day/Time, Room, Building, and Lecturer columns",
        widget=forms.FileInput(attrs={
            'accept': '.xlsx,.xls',
            'class': 'form-control-file'
        })
    )

    def clean_rooms_file(self):
        file = self.cleaned_data.get('rooms_file')
        if file:
            if not file.name.endswith(('.xlsx', '.xls')):
                raise ValidationError("Please upload an Excel file (.xlsx or .xls)")
            if file.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("File size cannot exceed 5MB")
        return file

    def clean_timetable_file(self):
        file = self.cleaned_data.get('timetable_file')
        if file:
            if not file.name.endswith(('.xlsx', '.xls')):
                raise ValidationError("Please upload an Excel file (.xlsx or .xls)")
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                raise ValidationError("File size cannot exceed 10MB")
        return file

    def clean(self):
        cleaned_data = super().clean()
        rooms_file = cleaned_data.get("rooms_file")
        timetable_file = cleaned_data.get("timetable_file")
        if not rooms_file and not timetable_file:
            raise forms.ValidationError(
                "At least one file (rooms or timetable) must be uploaded.")
        return cleaned_data
