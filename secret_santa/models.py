from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from decimal import Decimal

CURRENCY = ((0, "€"), (1, "£"), (2, "$"))

class Event(models.Model):
    """
    Represents an event related to a user, storing data
    like title, description, and an optional fields such as budget, date and image.
    """    
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True, blank=True)
    currency = models.IntegerField(choices=CURRENCY, default=0)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    event_image = CloudinaryField('image', default='placeholder')
    event_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Participant(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participant_profile')      
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=100)
    wishlist = models.TextField(blank=True, null=True)
    
    assigned_recipient = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='gifter'
    )

    def __str__(self):
        return f"{self.name} ({self.event.name})"