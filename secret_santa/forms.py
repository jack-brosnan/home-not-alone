from cloudinary.forms import CloudinaryFileField
from django import forms
from django.core.exceptions import ValidationError
from .models import Event, Participant


class EventForm(forms.ModelForm):
    """
    Form for adding or editing an events.
    """
    class Meta:
        """
        **Model**: :model:`Event`

        **Fields**:

        1. ``title``: Text field for entering the item name.
        2. ``description``: TextInput for entering a description.
        3. ``event_image``: File input for uploading an image.
        4. ``currency``: Dropdown field to select the currency.
        5. ``budget``: Decimal to select event budget.

        """
        model = Event
        fields = ['title', 'description', 'event_image', 'currency', 'budget']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title'}),
            'description': forms.TextInput(
                attrs={'placeholder': 'Enter Description'}
            ),
        }

class ParticipantForm(forms.ModelForm):
    """
    Form for adding or editing a participant.
    """
    class Meta:
        model = Participant
        fields = ['name', 'email']  # Include the email field here
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        }

class ParticipantWishlistForm(forms.ModelForm):
    """
    Form for particapant to update wishlist.
    """
    class Meta:
        model = Participant
        fields = ['wishlist']
        widgets = {
            'wishlist': forms.Textarea(attrs={'placeholder': 'Enter your wishlist items...'})
        }
