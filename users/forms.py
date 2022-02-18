from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Message, Skill


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'required': '', 'id': 'first-name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'required': '', 'id': 'last-name'})
        self.fields['username'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'required': '', 'id': 'username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'id': 'email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'id': 'password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'id': 'confirm-password'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['id', 'user', 'created']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'id': 'first-name', 'class': 'bg-tertiary input form__input'})
        self.fields['last_name'].widget.attrs.update(
            {'id': 'last-name', 'class': 'bg-tertiary input form__input'})
        self.fields['username'].widget.attrs.update(
            {'id': 'username', 'class': 'bg-tertiary input form__input'})
        self.fields['email'].widget.attrs.update(
            {'id': 'email', 'class': 'bg-tertiary input form__input'})
        self.fields['headline'].widget.attrs.update(
            {'id': 'headline', 'class': 'bg-tertiary input form__input'})
        self.fields['bio'].widget.attrs.update(
            {'id': 'bio', 'class': 'bg-tertiary input form__input'})
        self.fields['image'].widget.attrs.update({'id': 'image'})
        self.fields['location'].widget.attrs.update(
            {'id': 'location', 'class': 'bg-tertiary input form__input'})
        self.fields['github'].widget.attrs.update(
            {'id': 'github', 'class': 'bg-tertiary input form__input'})
        self.fields['linkedin'].widget.attrs.update(
            {'id': 'linkedin', 'class': 'bg-tertiary input form__input'})
        self.fields['twitter'].widget.attrs.update(
            {'id': 'twitter', 'class': 'bg-tertiary input form__input'})
        self.fields['youtube'].widget.attrs.update(
            {'id': 'youtube', 'class': 'bg-tertiary input form__input'})
        self.fields['website'].widget.attrs.update(
            {'id': 'website', 'class': 'bg-tertiary input form__input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['first_name', 'last_name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'id': 'message-first-name', 'class': 'bg-tertiary input form__input', 'required': ''})
        self.fields['last_name'].widget.attrs.update(
            {'id': 'message-last-name', 'class': 'bg-tertiary input form__input', 'required': ''})
        self.fields['email'].widget.attrs.update(
            {'id': 'message-email', 'class': 'bg-tertiary input form__input'})
        self.fields['subject'].widget.attrs.update(
            {'id': 'message-subject', 'class': 'bg-tertiary input form__input', 'required': ''})
        self.fields['body'].widget.attrs.update(
            {'id': 'message-body', 'class': 'bg-tertiary input form__input form__input_textbox', 'required': ''})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'id': 'skill-name', 'class': 'bg-tertiary input form__input', 'required': ''})
        self.fields['description'].widget.attrs.update(
            {'id': 'skill-description', 'class': 'bg-tertiary input form__input form__input_textbox'})
