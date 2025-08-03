from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=100)  # e.g., "A101"
    building = models.CharField(max_length=100)  # e.g., "A"
    capacity = models.PositiveIntegerField(default=0)
    amenities = models.JSONField(default=list)  # e.g., ["Projector", "Whiteboard"]
    photo_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "name",
                    "building"],
                name="unique_room_building")]

    def __str__(self):
        return f"{self.building}-{self.name}"

    def get_absolute_url(self):
        return f"/rooms/{self.name}"


class ClassSchedule(models.Model):
    course = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    DAY_CHOICES = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
    ]
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="schedules")
    lecturer = models.CharField(max_length=100)
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Class Schedule"
        verbose_name_plural = "Class Schedules"
        indexes = [
            models.Index(fields=["day", "start_time", "end_time"]),
            models.Index(fields=["room", "is_cancelled"]),
        ]

    def __str__(self):
        return (f"{self.course} {self.day} "
                f"({self.start_time} - {self.end_time}) "
                f"in {self.room}")

    def get_absolute_url(self):
        return f"/schedules/{self.id}"
