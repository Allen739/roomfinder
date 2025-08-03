import pandas as pd
from django.core.management.base import BaseCommand
from finder.models import Room
import json

class Command(BaseCommand):
    help = "Load rooms from rooms.xlsx into Room model."

    def handle(self, *args, **options):
        Room.objects.all().delete()

        try:
            df = pd.read_excel("sample_data/rooms.xlsx")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("rooms.xlsx not found in sample_data folder."))
            return

        expected_columns = {"Room", "Building", "capacity", "amenities", "photo_url"}
        if not all(col in df.columns for col in expected_columns):
            self.stdout.write(self.style.ERROR(f"Excel file must contain columns: {expected_columns}"))
            return

        created_count = 0
        for _, row in df.iterrows():
            room_name = str(row["Room"]).strip()
            building = str(row["Building"]).strip()
            capacity = int(row["capacity"])
            amenities_str = str(row["amenities"])
            photo_url = str(row["photo_url"]).strip()

            if not room_name or not building:
                self.stdout.write(self.style.WARNING(f"Skipping invalid row: Room={room_name}, Building={building}"))
                continue

            try:
                amenities = json.loads(amenities_str)
            except json.JSONDecodeError:
                self.stdout.write(self.style.WARNING(f"Skipping row with invalid amenities JSON: {amenities_str}"))
                continue

            Room.objects.update_or_create(
                name=room_name,
                building=building,
                defaults={
                    "capacity": capacity,
                    "amenities": amenities,
                    "photo_url": photo_url
                }
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {created_count} rooms into the database."))
