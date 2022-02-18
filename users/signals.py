from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

from django.core.mail import send_mail
from django.conf import settings

from .models import Profile


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance

        profile = Profile.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username.lower(),
            email=user.email
        )

        subject = 'DevSearch'
        message = f'Thank you for signing up, {profile.first_name}.\n\nWe built devgalaxy.ir to provide a place to connect to other developers, visit their projects and share your projects to make others see.\n\nWe are glad you joined our website.'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def update_user(sender, instance, created, **kwargs):
    if not created:
        profile = instance
        user = profile.user

        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.username = profile.username

        if profile.email:
            user.email = profile.email

        user.save()


def delete_user(sender, instance, **kwargs):
    profile = instance
    user = profile.user
    user.delete()


post_save.connect(create_profile, sender=User)
post_save.connect(update_user, sender=Profile)
post_delete.connect(delete_user, sender=Profile)
