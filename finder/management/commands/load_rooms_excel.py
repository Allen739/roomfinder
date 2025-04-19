import pandas as pd
from django.core.management.base import BaseCommand
from finder.models import Room

class Command(BaseCommand):
    help = "Load rooms from rooms.xlsx into Room model."

    def handle(self, *args, **options):
        # Clear existing rooms (for testing)
        Room.objects.all().delete()

        # Read the Excel file
        try:
            df = pd.read_excel("rooms.xlsx")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("rooms.xlsx not found in project root."))
            return
        
        # Validate the DataFrame
        expected_columns = {"Room", "Building"}
        if not all(col in df.columns for col in expected_columns):
            self.stdout.write(self.style.ERROR(f"Excel file must contain columns: {expected_columns}"))
            return
        
        # Process each row
        created_count = 0
        for _, row in df.iterrows():
            room_name = str(row["Room"]).strip()
            building = str(row["Building"]).strip()


            # Validate room name and building name
            if not room_name or not building:
                self.stdout.write(self.style.WARNING(f"Skipping invalid row: Room={room_name}, Building={building}"))
                continue

            # Create or update Room
            Room.objects.update_or_create(
                name = room_name,
                building = building,
                defaults={"name": room_name, "building": building}
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {created_count} rooms into the database."))