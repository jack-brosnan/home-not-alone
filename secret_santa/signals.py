from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def add_user_to_organiser_group(sender, instance, created, **kwargs):
    if created and instance.is_active:
        # Any newly registered user is an organiser
        organiser_group, created_group = Group.objects.get_or_create(name='Organiser')
        instance.groups.add(organiser_group)