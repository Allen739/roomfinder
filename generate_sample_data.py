import pandas as pd
import random
import json

# --- Configuration ---
NUM_ROOMS = 50
NUM_SCHEDULES = 300
BUILDINGS = {
    "Hephaestus Hall": "HH",
    "Athena Tower": "AT",
    "Prometheus Center": "PC",
    "Apollo Building": "AB",
    "Artemis Wing": "AW",
}
AMENITIES_LIST = ["Projector", "Whiteboard", "Podium", "Speakers", "Smart Board", "Conference Phone"]
PHOTO_URLS = [
    'https://images.unsplash.com/photo-1567589008473-76c02936a352?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    'https://images.unsplash.com/photo-1590479600959-a3e27943c433?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    'https://images.unsplash.com/photo-1563245929-176bf0575475?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    'https://images.unsplash.com/photo-1519125323398-675f0ddb6308?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
]
COURSES = ["CS101", "MA203", "PY101", "EN205", "HI301", "BI210", "CH330", "EC401"]
SUBJECTS = ["Intro to Programming", "Calculus III", "General Physics", "British Literature", "World History", "Cell Biology", "Organic Chemistry", "Macroeconomics"]
LECTURERS = ["Dr. Smith", "Prof. Jones", "Dr. Williams", "Prof. Brown", "Dr. Davis", "Prof. Miller", "Dr. Wilson", "Prof. Moore"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# --- Generate Rooms Data ---
rooms_data = []
for i in range(NUM_ROOMS):
    building_name, building_code = random.choice(list(BUILDINGS.items()))
    room_number = f"{building_code}{random.randint(100, 499)}"
    capacity = random.choice([20, 25, 30, 40, 50, 60, 100])
    num_amenities = random.randint(1, 4)
    amenities = json.dumps(random.sample(AMENITIES_LIST, num_amenities))
    photo_url = random.choice(PHOTO_URLS)
    rooms_data.append([room_number, building_name, capacity, amenities, photo_url])

rooms_df = pd.DataFrame(rooms_data, columns=["Room", "Building", "capacity", "amenities", "photo_url"])

# --- Generate Timetable Data ---
timetable_data = []
room_building_list = list(zip(rooms_df['Room'], rooms_df['Building']))

for _ in range(NUM_SCHEDULES):
    course = random.choice(COURSES)
    subject = random.choice(SUBJECTS)
    lecturer = random.choice(LECTURERS)
    day = random.choice(DAYS)
    
    start_hour = random.randint(7, 20)
    duration_hours = random.choice([1, 1.5, 2])
    start_time = f"{start_hour:02d}:{random.choice(['00', '30'])}"
    end_hour = int(start_hour + duration_hours)
    end_minute = int((start_hour + duration_hours) % 1 * 60)
    end_time = f"{end_hour:02d}:{end_minute:02d}"
    
    day_time = f"{day} {start_time}-{end_time}"
    
    room, building = random.choice(room_building_list)
    
    timetable_data.append([course, subject, day_time, room, building, lecturer])

timetable_df = pd.DataFrame(timetable_data, columns=["Course", "Subject", "Day/Time", "Room", "Building", "Lecturer"])

# --- Save to Excel ---
rooms_df.to_excel("sample_data/rooms.xlsx", index=False)
timetable_df.to_excel("sample_data/timetable.xlsx", index=False)

print("Successfully generated new sample_data/rooms.xlsx and sample_data/timetable.xlsx")