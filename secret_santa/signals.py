from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from allauth.account.signals import user_signed_up, user_logged_in
from invitations.signals import invite_accepted
from invitations.utils import get_invitation_model
from .models import Participant

Invitation = get_invitation_model()

@receiver(user_signed_up)
def set_organiser_role_on_signup(sender, request, user, **kwargs):
    """
    When a user registers without an invitation, 
    they are assigned the role of 'organiser'.
    """
    organiser_group, _ = Group.objects.get_or_create(name='Organiser')
    user.groups.add(organiser_group)

@receiver(invite_accepted)
def handle_invite_accepted(sender, email, invitation, request, **kwargs):
    """
    After user has signed up after clicking the invitation link,
    they are assigned the role of 'participant'. The newly created 
    user record is then to the matching participant record.
    """
    user = User.objects.filter(email__iexact=email).first()
    if user:
        
        try:
            # Connect the invited user to their Participant profile if it exists
            participant = Participant.objects.get(email__iexact=email, user__isnull=True)
            participant.user = user
            participant.save()
        except Participant.DoesNotExist:
            # If no Participant record exists for this email, we still treat them as a participant user
            pass
            
        #Updates user role to 'participant
        participant_group, _ = Group.objects.get_or_create(name='Participant')
        user.groups.add(participant_group)
        organiser_group, _ = Group.objects.get_or_create(name='Organiser')
        user.groups.remove(organiser_group)