# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User, Group
# from invitations.signals import invite_accepted
# from .models import Participant

# @receiver(post_save, sender=User)
# def add_user_to_organiser_group(sender, instance, created, **kwargs):
#     if created and instance.is_active:
#         # Any newly registered user is an organiser
#         organiser_group, created_group = Group.objects.get_or_create(name='Organiser')
#         instance.groups.add(organiser_group)

from django.dispatch import receiver
from invitations.signals import invite_accepted
from django.contrib.auth.models import Group
from .models import Participant

@receiver(invite_accepted)
def handle_invite_accepted(sender, email, request, invitation, **kwargs):
    """
    Link the new User to the Participant record and assign them to the Participant group.
    """
    print(f"Signal Triggered: email={email}, invitation={invitation}")  # Debugging

    try:
        # Find the participant linked to this email
        participant = Participant.objects.get(email=email, user__isnull=True)
        
        # The `request.user` should be the user who just signed up and accepted the invite
        participant.user = request.user
        participant.save()

        # Add the user to the Participant group
        group, created = Group.objects.get_or_create(name="Participant")
        request.user.groups.add(group)

        print(f"User {request.user.username} linked to Participant {participant.name}")  # Debugging
    except Participant.DoesNotExist:
        print(f"No Participant found for email {email}")  # Debugging