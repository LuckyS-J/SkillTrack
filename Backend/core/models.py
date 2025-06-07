from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Address(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    post_code = models.CharField(max_length=10)
    street = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.post_code} {self.city}, {self.country}"


class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category or 'No category'})"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, related_name="user_profile", blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name="user_skills")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class StudySession(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sessions")
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    duration = models.DurationField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session of {self.user.username} for {self.skill.name} on {self.date}"