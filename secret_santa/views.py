from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from .models import Participant, Event
import random, string


class HomePage(TemplateView):
    """
    Displays home page"
    """
    template_name = 'index.html'
    
def create_participant_for_event(event, participant_name):
    
    username = generate_unique_username(participant_name)
    password = User.objects.make_random_password()
    user = User.objects.create_user(username=username, password=password)
    
    
    participant_group, _ = Group.objects.get_or_create(name='Participant')
    user.groups.add(participant_group)
    
    
    participant = Participant.objects.create(
        user=user,
        event=event,
        name=participant_name,
    )

    return participant

def generate_unique_username(name):
    suffix = ''.join(random.choices(string.digits, k=4))
    base_username = name.lower().replace(' ', '_')
    return f"{base_username}_{suffix}"