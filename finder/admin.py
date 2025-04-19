from django.contrib import admin
from .models import Room, ClassSchedule
# Register your models here.

@admin.register(Room)
class Roomadmin(admin.ModelAdmin):
    list_display = ("name", "building")
    search_fields = ("name", "building")
    list_filter = ("building",)
    ordering = ("building", "name")

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ("course", "subject", "day", "start_time", "end_time", "room", "lecturer", "is_cancelled")
    list_filter = ("day", "room__building","is_cancelled")
    search_fields = ("course", "subject", "lecturer")
    list_editable = ("is_cancelled", "room")
    ordering = ("day", "start_time")
    actions = ["cancel_classes", "restore_classes"]

    def cancel_classes(self, request, queryset):
        queryset.update(is_cancelled=True)
        self.message_user(request, f"Cancelled {queryset.count()} classes.")
    cancel_classes.short_description = "Cancel selected classes"

    def restore_classes(self, request, queryset):
        queryset.update(is_cancelled=False)
        self.message_user(request, f"Restored {queryset.count()} classes.")
    restore_classes.short_description = "Restore selected classes"