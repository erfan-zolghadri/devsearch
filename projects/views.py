from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utilities import paginate_queryset
from .forms import ProjectForm, ReviewForm
from .models import Project
from .utilities import search_projects, set_project_tags


def projects(request):
    search = request.GET.get('search', '')

    projects = search_projects(search)
    projects, page_range = paginate_queryset(request, projects)

    context = {
        'projects': projects,
        'search': search,
        'page_range': page_range
    }

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    context = {
        'project': project,
        'form': form
    }

    return render(request, 'projects/project.html', context)


@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.profile = request.user.profile
            project.save()

            set_project_tags(request, project)

            messages.info(request, 'Project has been added.')
            return redirect('account')
        else:
            messages.error(request, 'An unexpected error has ocurred.')

    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    context = {
        'form': form,
        'project': project
    }

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            set_project_tags(request, project)
            project.save()
            messages.info(request, 'Project has been edited.')
            return redirect('account')
        else:
            messages.error(request, 'An unexpected error has ocurred.')

    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    context = {
        'object': project
    }

    if request.method == 'POST':
        project.delete()
        messages.info(request, 'Project has been deleted.')
        return redirect('account')

    return render(request, 'delete.html', context)


@login_required(login_url='login')
def create_review(request, pk):
    project = Project.objects.get(id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.profile = request.user.profile
            review.project = project
            review.save()
            project.update_votes
            messages.info(request, 'Review has been added.')
            return redirect('project', pk=project.id)