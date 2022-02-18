from django.db.models import Q
from .models import Profile, Skill


def search_profiles(search):
    if search:
        skills = Skill.objects.filter(name__iexact=search)
        profiles = Profile.objects.distinct().filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(headline__icontains=search) |
            Q(skill__in=skills)
        ).order_by('first_name', 'last_name', '-created')
    else:
        profiles = Profile.objects.exclude(
            Q(headline__isnull=True) |
            Q(bio='')
        ).order_by(
            '-created', 'first_name', 'last_name')

    return profiles
