from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Event, Participant

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'organiser',
        'title',
        'description',
        'currency',
        'budget',
        'event_image',
        'event_date',
        'created_at',
        'updated_on',
        )


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user',
                    'event',
                    'name',
                    'wishlist',
                    'assigned_recipient',
                    )