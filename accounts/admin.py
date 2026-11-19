from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import StudentProfile, TeacherProfile


# =========================
# Teacher Admin
# =========================

class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    extra = 1


class TeacherUserAdmin(UserAdmin):
    inlines = [TeacherProfileInline]

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )


# =========================
# Student Profile Admin
# =========================

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone",
    )

    ordering = ("-created_at",)


# =========================
# Teacher Profile Admin
# =========================

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone",
    )

    ordering = ("-created_at",)