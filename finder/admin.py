from django.contrib import admin
from .models import Room, ClassSchedule
# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'get_schedule_count']
    list_filter = ['building']
    search_fields = ['name', 'building']
    ordering = ['building', 'name']
    
    def get_schedule_count(self, obj):
        return obj.schedules.count()
    get_schedule_count.short_description = 'Scheduled Classes'


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'course', 'subject', 'day', 'start_time', 'end_time', 
        'room', 'lecturer', 'is_cancelled'
    ]
    list_filter = [
        'day', 'is_cancelled', 'room__building', 
        'start_time', 'end_time'
    ]
    search_fields = [
        'course', 'subject', 'lecturer', 
        'room__name', 'room__building'
    ]
    list_editable = ['is_cancelled']
    ordering = ['day', 'start_time', 'room']
    date_hierarchy = None
    
    fieldsets = (
        ('Course Information', {
            'fields': ('course', 'subject', 'lecturer')
        }),
        ('Schedule Details', {
            'fields': ('day', 'start_time', 'end_time', 'room')
        }),
        ('Status', {
            'fields': ('is_cancelled',)
        }),
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('room')


# Custom admin site configuration
admin.site.site_header = "Campuspal Room Finder Admin"
admin.site.site_title = "Room Finder Admin"
admin.site.index_title = "Welcome to Room Finder Administration"
