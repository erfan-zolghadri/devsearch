from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from utilities import paginate_queryset, summarize_text
from .forms import CustomUserCreationForm, MessageForm, ProfileForm, SkillForm
from .models import Profile
from .utilities import search_profiles


def index(request):
    search = request.GET.get('search', '')

    profiles = search_profiles(search)
    profiles, page_range = paginate_queryset(request, profiles)

    for profile in profiles:
        if (profile.bio) and (len(profile.bio) > 100):
            profile.bio = summarize_text(profile.bio)

    context = {
        'profiles': profiles,
        'search': search,
        'page_range': page_range
    }

    return render(request, 'users/index.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'Username or password is incorrect.')

    return render(request, 'users/login-register.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('index')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    page = 'register'
    form = CustomUserCreationForm()
    context = {
        'page': page,
        'form': form
    }

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(
                request, 'Your account has been successfully created.')
            login(request, user)
            return redirect('edit-profile')
        else:
            messages.error(request, form.errors)

    return render(request, 'users/login-register.html', context)


@login_required(login_url='login')
def account(request):
    profile = request.user.profile
    skills_with_description = profile.skill_set.exclude(description='')
    skills_without_description = profile.skill_set.filter(description='')
    context = {
        'profile': profile,
        'skills_with_description': skills_with_description,
        'skills_without_description': skills_without_description
    }

    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def update_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.username = profile.username.lower()
            profile.save()
            messages.info(request, 'Profile has been edited.')
            return redirect('account')
        else:
            messages.error(request, 'An unexpected error has ocurred.')

    return render(request, 'users/profile-form.html', context)


@login_required(login_url='login')
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')

        if user.check_password(password):
            user.profile.delete()
            messages.info(request, 'Account has been successfully deleted.')
            return redirect('index')
        else:
            messages.error(request, 'Password is incorrect.')

    return render(request, 'users/delete-account.html')


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    skills_with_description = profile.skill_set.exclude(description='')
    skills_without_description = profile.skill_set.filter(description='')
    context = {
        'profile': profile,
        'skills_with_description': skills_with_description,
        'skills_without_description': skills_without_description
    }

    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def create_skill(request):
    form = SkillForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = request.user.profile
            skill.save()
            messages.info(request, 'Skill has been added.')
            return redirect('account')
        else:
            messages.error(request, 'An unexpected error has ocurred.')

    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.info(request, 'Skill has been edited.')
            return redirect('account')
        else:
            messages.error(request, 'An unexpected error has ocurred.')

    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    context = {
        'object': skill
    }

    if request.method == 'POST':
        skill.delete()
        messages.info(request, 'Skill has been deleted.')
        return redirect('account')

    return render(request, 'delete.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    message_objects = profile.messages.all().order_by('is_read', '-created')
    unread_messages_count = profile.messages.filter(is_read=False).count()
    context = {
        'message_objects': message_objects,
        'unread_messages_count': unread_messages_count
    }

    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    message.is_read = True
    message.save()

    context = {
        'message': message
    }

    return render(request, 'users/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    context = {
        'recipient': recipient,
        'form': form
    }

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            if request.user.is_authenticated:
                profile = request.user.profile
                message.sender = profile
                message.first_name = profile.first_name
                message.last_name = profile.last_name
                message.email = profile.email
            else:
                message.sender = None
            message.recipient = recipient

            message.save()
            messages.success(
                request, 'Your message has been successfully sent.')

            return redirect('profile', pk=recipient.id)
        else:
            messages.error(request, 'An unexpected error has ocurred.')

    return render(request, 'users/message-form.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    context = {
        'object': message
    }

    if request.method == 'POST':
        message.delete()
        messages.info(request, 'Message has been deleted.')
        return redirect('inbox')

    return render(request, 'delete.html', context)