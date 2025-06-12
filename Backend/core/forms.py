from django import forms
from .models import StudySession, Skill, UserProfile
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class StudySessionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields["skill"].queryset = Skill.objects.filter(user=user)
        for field in self.fields.values():
            field.widget.attrs.update(
                {'class': 'form-control bg-dark text-light border-secondary'})

    DURATION_CHOICES = [
        (timedelta(minutes=15), "15 minutes"),
        (timedelta(minutes=30), "30 minutes"),
        (timedelta(minutes=45), "45 minutes"),
        (timedelta(hours=1), "1 hour"),
        (timedelta(hours=1, minutes=30), "1.5 hours"),
        (timedelta(hours=2), "2 hours"),
        (timedelta(hours=2, minutes=30), "2.5 hours"),
        (timedelta(hours=3), "3 hours")
    ]

    duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        label="Duration of session",
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
        }),
        label="Date of session"
    )

    class Meta:
        model = StudySession
        fields = ["skill", "date", "duration", "notes"]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class SkillForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {'class': 'form-control bg-dark text-light border-secondary'})

    CATEGORY_CHOICES = [
        ("cognitive", "Cognitive Skills"),
        ("programming", "Programming / Coding"),
        ("data_analysis", "Data Analysis"),
        ("languages", "Foreign Languages"),
        ("writing", "Writing & Composition"),
        ("public_speaking", "Public Speaking"),
        ("project_management", "Project Management"),
        ("design", "Design & Creativity"),
        ("math", "Mathematics"),
        ("science", "Science & Engineering"),
        ("history", "History & Culture"),
        ("time_management", "Time Management"),
        ("communication", "Communication Skills"),
        ("productivity", "Productivity Techniques"),
        ("critical_thinking", "Critical Thinking"),
        ("memory_training", "Memory Training"),
        ("music", "Music & Instruments"),
        ("art", "Art & Drawing"),
        ("soft_skills", "Soft Skills"),
        ("mindfulness", "Mindfulness & Well-being"),
        ("other", "Other")
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label="Skill category",
        initial="other"
    )

    class Meta:
        model = Skill
        fields = ["name", "description", "category"]
        widgets = {
            "description": forms.Textarea(attrs={'rows': 3}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {'class': 'form-control bg-dark text-light border-secondary'})


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {'class': 'form-control bg-dark text-light border-secondary'})
            
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us something about yourself...',
                'class': 'form-control'
            }),
        }
        labels = {
            'bio': 'Bio',
            'profile_picture': 'Profile Picture'
        }