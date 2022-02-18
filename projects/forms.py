from django.forms import ModelForm
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'source_link', 'demo_link']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'required': '', 'id': 'project-title'})
        self.fields['description'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'id': 'project-description'})
        self.fields['source_link'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'id': 'project-source-link'})
        self.fields['demo_link'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'id': 'project-demo-link'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['vote', 'comment']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['vote'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input', 'required': ''})
        self.fields['comment'].widget.attrs.update(
            {'class': 'bg-tertiary input form__input form__input_textbox', 'placeholder': 'Write your comments here...'})
