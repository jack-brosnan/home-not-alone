from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from .models import Participant, Event
from .forms import EventForm, ParticipantForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
import random, string
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from invitations.utils import get_invitation_model


def is_organiser(user):
    return user.groups.filter(name="Organiser").exists()

Invitation = get_invitation_model()


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

@user_passes_test(is_organiser)
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
    Display the details of a specific Event along with its participants.
    """
    event = get_object_or_404(Event, pk=event_id, organiser=request.user)
    participants = Participant.objects.filter(event=event)

    return render(
        request,
        'secret_santa/view_event.html',
        {
            "event": event,
            "participant": participants,
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

