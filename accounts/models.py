
from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )

    can_add_teacher = models.BooleanField(default=False)

    
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="teachers/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username