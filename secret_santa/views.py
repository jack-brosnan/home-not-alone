from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from invitations.utils import get_invitation_model
import random
from .models import Participant, Event
from .forms import EventForm, ParticipantForm, ParticipantWishlistForm

Invitation = get_invitation_model()

# Used to check and display content related to the user with a 'organiser' group designation
def is_organiser(user):
    return user.is_authenticated and user.groups.filter(name='Organiser').exists()

# Used to check and display content related to the user with a 'participant' group designation
def is_participant(user):
    return user.is_authenticated and user.groups.filter(name='Participant').exists()

@method_decorator(login_required, name='dispatch')
class EventList(View):
    """
    Displays the main page differently based on user role:
    - Organiser: Shows event list and option to create and manage events.
    - Participant: Shows participant portal with event details, recipient, and wishlist form.
    """
    template_name = "secret_santa/index.html"

    def get(self, request, *args, **kwargs):
        # Displays either participant portal or organiser content on index page based on user role
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Form to update wishlist if logged in as 'participant'
        if is_participant(request.user):
            participant = Participant.objects.get(user=request.user)
            form = ParticipantWishlistForm(request.POST, instance=participant)
            if form.is_valid():
                form.save()
                messages.success(request, "Your wishlist has been updated!")
            return redirect('/')
        return redirect('/')

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = {}

        if is_organiser(user):
            events = Event.objects.filter(organiser=user).order_by("-created_at")
            context['events'] = events
            context['is_organiser'] = True
            context['is_participant'] = False
        elif is_participant(user):
            participant = get_object_or_404(Participant, user=user)
            event = participant.event
            assigned_recipient = participant.assigned_recipient
            form = ParticipantWishlistForm(instance=participant)

            context['is_organiser'] = False
            context['is_participant'] = True
            context['event'] = event
            context['participant'] = participant
            context['assigned_recipient'] = assigned_recipient
            context['form'] = form
        else:
            context['events'] = None
            context['is_organiser'] = False
            context['is_participant'] = False

        return context

@login_required
@user_passes_test(is_organiser, login_url='home')
def add_event(request):
    """
    Allows an organiser to create a new event.
    Checks for valid form submission and saves a new event linked to the organiser.
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

    return render(request, "secret_santa/add_event.html", {"event_form": event_form})

@login_required
def edit_event(request, edit_id):
    """
    Allows an organiser to edit an existing event.
    Redirects back to index page on success.
    """
    event = get_object_or_404(Event, pk=edit_id, organiser=request.user)

    if request.method == "POST":
        event_form = EventForm(request.POST, request.FILES, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated!")
            return HttpResponseRedirect(reverse("home"))
        messages.error(request, "Error updating event!")
    else:
        event_form = EventForm(instance=event)

    return render(request, "secret_santa/edit_event.html", {
        "event_form": event_form,
        "edit_id": edit_id,
    })

@login_required
def delete_event(request, event_id):
    """
    Allows an organiser to delete an event.
    On POST confirmation, deletes the event and redirects to home.
    """
    event = get_object_or_404(Event, pk=event_id, organiser=request.user)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
    return redirect("home")

@login_required
def view_event(request, event_id):
    """
    Allows an organiser to view details 
    of a specific event and added participants.    
    """
    event = get_object_or_404(Event, pk=event_id, organiser=request.user)
    participants = Participant.objects.filter(event=event)
    is_organiser_flag = request.user.is_authenticated and request.user.groups.filter(name="Organiser").exists()

    return render(request, 'secret_santa/view_event.html', {
        "event": event,
        "participant": participants,
        "is_organiser": is_organiser_flag
    })

@login_required
def edit_participant(request, event_id):
    """
    Allows an organiser to manage participants for an event:
    - Add new participants
    - Edit existing participants' details
    - Delete participants
    """
    event = get_object_or_404(Event, pk=event_id, organiser=request.user)
    participants = Participant.objects.filter(event=event)
    form = ParticipantForm()

    if request.method == 'POST':
        # Opens form to edit existing participant
        if 'edit' in request.POST:
            pk = request.POST.get('edit')
            participant = get_object_or_404(Participant, id=pk, event=event)
            form = ParticipantForm(instance=participant)

        # Update existing participant
        elif 'save' in request.POST:
            pk = request.POST.get('save')
            if pk:
                participant = get_object_or_404(Participant, id=pk, event=event)
                form = ParticipantForm(request.POST, instance=participant)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Participant edited!')
            else:
                # Create a new participant
                form = ParticipantForm(request.POST)
                if form.is_valid():
                    new_participant = form.save(commit=False)
                    new_participant.event = event
                    new_participant.save()
                    messages.success(request, 'Participant added!')
            form = ParticipantForm()
        # Delete a participant
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            if pk:
                participant = get_object_or_404(Participant, id=pk, event=event)
                participant.delete()
                messages.success(request, 'Participant deleted!')
        # Cancel and redirect to view_event page
        elif 'cancel' in request.POST:
            return redirect('edit_participant', event_id=event_id)

    return render(request, 'secret_santa/edit_participant.html', {
        'event': event,
        'participants': participants,
        'form': form,
    })

@login_required
def random_santa(request, event_id):
    """
    Organiser can randomly assign participants to each other.
    Ensures there are enough participants before shuffling and assigning.
    Once assigned, each participant's 'assigned_recipient' field is updated.
    """
    event = get_object_or_404(Event, pk=event_id, organiser=request.user)
    participants = list(Participant.objects.filter(event=event))

    if len(participants) < 2:
        messages.error(request, "Not enough participants to assign recipients.")
        return redirect('view_event', event_id=event.id)

    random.shuffle(participants)

    for i in range(len(participants)):
        santa = participants[i]
        recipient = participants[(i + 1) % len(participants)]
        santa.assigned_recipient = recipient
        santa.save()

    messages.success(request, "Recipients assigned successfully!")
    return redirect('view_event', event_id=event.id)

def is_organiser(user):
    return user.is_authenticated and user.groups.filter(name='Organiser').exists()

@login_required
@user_passes_test(is_organiser, login_url='home')
def invite_participant(request, participant_id):
    """
    Allows an organiser to send an invitation email to a participant who does not yet have a user account.
    Sends an invite link to the participant's email address.
    """
    participant = get_object_or_404(Participant, id=participant_id, event__organiser=request.user)
    if participant.email:
        try:
            invitation = Invitation.create(email=participant.email, inviter=request.user)
            invitation.send_invitation(request)
            messages.success(request, f"Invitation link sent to {participant.email}!")
        except Exception as e:
            messages.error(request, f"Failed to send invitation to {participant.email}. An email has already been sent")
    else:
        messages.error(request, "Participant has no email specified.")

    return redirect('view_event', event_id=participant.event.id)

def is_participant(user):
    return user.is_authenticated and user.groups.filter(name='Participant').exists()

@login_required
@user_passes_test(is_participant, login_url='home')
def participant_portal(request):
    """
    Displays the participant view that includes their assigned giftee and wishlist 
    Also includes wishlish form for the logged in participant to updated
    """
    # Participant can view their event, assigned recipient, and update their wishlist
    participant = get_object_or_404(Participant, user=request.user)
    event = participant.event
    assigned_recipient = participant.assigned_recipient

    if request.method == 'POST':
        form = ParticipantWishlistForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Your wishlist has been updated!")
            return redirect('participant_portal')
    else:
        form = ParticipantWishlistForm(instance=participant)

    return render(
        request,
        'secret_santa/participant_portal.html',
        {
            'event': event,
            'participant': participant,
            'assigned_recipient': assigned_recipient,
            'form': form,
        }
    )