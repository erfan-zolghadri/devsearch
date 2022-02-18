from django.db.models import Q
from .models import Project, Tag


def search_projects(search):
    if search:
        tags = Tag.objects.filter(name__iexact=search)
        projects = Project.objects.distinct().filter(
            Q(title__icontains=search) |
            Q(profile__first_name__icontains=search) |
            Q(profile__last_name__icontains=search) |
            Q(tags__in=tags)
        )
    else:
        projects = Project.objects.all().order_by('-created', 'title')

    return projects


def set_project_tags(request, project):
    tags = request.POST.get('project-tags').replace(',', ' ').split()
    for tag in tags:
        tag, created = Tag.objects.get_or_create(name=tag)
        project.tags.add(tag)
