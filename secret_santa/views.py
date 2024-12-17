from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from .models import Participant, Event
from .forms import EventForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import random, string
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse





class EventList(TemplateView):
    """
    Displays home page"
    """
    template_name = "secret_santa/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Authenticated users see their events
            context["events"] = Event.objects.filter(
                organiser=self.request.user
            ).order_by("-created_at")
        else:
            # Unauthenticated users see the welcome page
            context["events"] = None
        return context
    
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


@login_required
def add_event(request):
    """
    Add a new expense space.
    """
    if request.method == "POST":
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.organiser = request.user
            event.save()
            messages.success(request, "Event added successfully!")
            return redirect("home")
    else:
        event_form = EventForm()

    return render(
        request,
        "secret_santa/add_event.html",
        {"event_form": event_form},
    )


@login_required
def edit_event(request, edit_id):
    """
    Edit an existing event.
    """
    event = get_object_or_404(
                    Event,
                    pk=edit_id,
                    organiser=request.user
                    )

    if request.method == "POST":
        event_form = EventForm(
            data=request.POST,
            files=request.FILES,
            instance=event,
        )
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated!")
            return HttpResponseRedirect(reverse("home"))
        messages.error(request, "Error updating event!")
    else:
        event_form = EventForm(instance=event)

    return render(
        request,
        "secret_santa/edit_event.html",
        {
            "event_form": event_form,
            "edit_id": edit_id,
        },
    )


@login_required
def delete_event(request, event_id):
    """
    Delete an existing event.
    """
    event = get_object_or_404(Event,
                                      pk=event_id,
                                      organiser=request.user
                                      )
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
    return redirect("home")


@login_required
def view_event(request, event_id):
    """
    Display the details of a specific Event along with
    its linked EventLines.
    """
    event = get_object_or_404(
        Event,
        pk=event_id,
        organiser=request.user
        )

    participant = Participant.objects.filter(event=event)

    return render(
        request,
        'secret_santa/view_event.html',
        {
            "event": event,
            "participant": participant,
        }
    )