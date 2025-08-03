from django.http import JsonResponse
from .models import Room
import datetime

def room_details(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)

    day = request.GET.get('day', 'Mon') # Default to Monday if no day is provided
    schedules = room.schedules.filter(day=day, is_cancelled=False).order_by('start_time')

    timeline = []
    last_end_time = datetime.time(7, 0)

    for schedule in schedules:
        if schedule.start_time > last_end_time:
            timeline.append({
                "type": "free",
                "start": last_end_time.strftime("%H:%M"),
                "end": schedule.start_time.strftime("%H:%M"),
            })
        timeline.append({
            "type": "booked",
            "start": schedule.start_time.strftime("%H:%M"),
            "end": schedule.end_time.strftime("%H:%M"),
            "course": schedule.course,
            "subject": schedule.subject,
        })
        last_end_time = schedule.end_time
    
    if last_end_time < datetime.time(23, 0):
        timeline.append({
            "type": "free",
            "start": last_end_time.strftime("%H:%M"),
            "end": "23:00",
        })

    data = {
        "room": {
            "id": room.id,
            "name": room.name,
            "building": room.building,
            "capacity": room.capacity,
            "amenities": room.amenities,
            "photo_url": room.photo_url,
        },
        "timeline": timeline,
    }

    return JsonResponse(data)