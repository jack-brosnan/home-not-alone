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
        5. ``bydget``: Decimal to select event budget.

        """
        model = Event
        fields = ['title', 'description', 'event_image', 'currency', 'budget']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title'}),
            'description': forms.TextInput(
                attrs={'placeholder': 'Enter Description'}
            ),
        }