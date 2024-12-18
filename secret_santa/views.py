from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from .models import Participant, Event
from .forms import EventForm, ParticipantForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import random, string
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db import transaction




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
    
# def create_participant_for_event(event, participant_name):
    
#     username = generate_unique_username(participant_name)
#     password = User.objects.make_random_password()
#     user = User.objects.create_user(username=username, password=password)
    
    
#     participant_group, _ = Group.objects.get_or_create(name='Participant')
#     user.groups.add(participant_group)
    
    
#     participant = Participant.objects.create(
#         user=user,
#         event=event,
#         name=participant_name,
#     )

#     return participant

# def generate_unique_username(name):
#     suffix = ''.join(random.choices(string.digits, k=4))
#     base_username = name.lower().replace(' ', '_')
#     return f"{base_username}_{suffix}"


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

@login_required
def edit_participant(request, event_id):
    """
    Add, edit, or delete participants for an event.
    """
    event = get_object_or_404(
        Event,
        pk=event_id,
        organiser=request.user
    )

    participants = Participant.objects.filter(event=event)
    form = ParticipantForm()

    if request.method == 'POST':
        if 'edit' in request.POST:
            pk = request.POST.get('edit')
            participant = get_object_or_404(
                Participant,
                id=pk,
                event=event
            )
            form = ParticipantForm(instance=participant)

        elif 'save' in request.POST:
            pk = request.POST.get('save')
            if pk:
                # Editing existing participant
                participant = get_object_or_404(
                    Participant,
                    id=pk,
                    event=event
                )
                form = ParticipantForm(request.POST, instance=participant)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Participant edited!')
            else:
                # Creating a new participant
                form = ParticipantForm(request.POST)
                if form.is_valid():
                    new_participant = form.save(commit=False)
                    new_participant.event = event
                    # Additional logic for creating User if needed
                    new_participant.save()
                    messages.success(request, 'Participant added!')

            # Reset form after save
            form = ParticipantForm()

        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            if pk:
                participant = get_object_or_404(
                    Participant,
                    id=pk,
                    event=event
                )
                participant.delete()
                messages.success(request, 'Participant deleted!')

        elif 'cancel' in request.POST:
            return redirect('edit_participant', event_id=event_id)

    return render(
        request,
        'secret_santa/edit_participant.html',
        {
            'event': event,
            'participants': participants,
            'form': form,
        }
    )

@login_required
def random_santa(request, event_id):
    """
    Display the details of a specific Event along with
    its linked EventLines.
    """
    event = get_object_or_404(
        Event,
        pk=event_id,
        organiser=request.user
        )

    participants = list(Participant.objects.filter(event=event))

    if len(participants) < 2:
        messages.error(request, "Not enough participants to assign recipients.")
        return redirect('view_event', event_id=event.id)

    random.shuffle(participants)
    print(participants)

    # Save and save pairs

    for i in range(len(participants)):
        santa = participants[i]
        recipient = participants[(i + 1) % len(participants)]  # Next participant if the last is first
        santa.assigned_recipient = recipient
        santa.save()

    messages.success(request, "Recipients assigned successfully!")
    return redirect('view_event', event_id=event.id)
