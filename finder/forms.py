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

    building = forms.ChoiceField(
        label="Building",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_building'
        })
    )
    day = forms.ChoiceField(
        choices=DAYS, 
        label="Day",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_day'
        })
    )
    time = forms.TimeField(
        label="Start Time (Optional)",
        required=False,
        widget=forms.TimeInput(attrs={
            "type": "time",
            'class': 'form-control',
            'id': 'id_time'
        })
    )
    duration = forms.IntegerField(
        label="Duration (minutes, optional)",
        required=False,
        min_value=15,
        max_value=480, # 8 hours
        help_text="Enter duration in minutes (e.g., 60 for 1 hour). Min 15, Max 480.",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_duration',
            'placeholder': 'e.g., 60',
            'step': '15'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        buildings = Room.objects.values('building').distinct().order_by('building')
        building_choices = [("ALL", "All Buildings")] + [
            (b["building"], b["building"]) for b in buildings
        ]
        self.fields["building"].choices = building_choices


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
