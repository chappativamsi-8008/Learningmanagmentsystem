
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from courses.models import Course

from .forms import StudentRegistrationForm, TeacherRegistrationForm
from courses.models import Enrollment,LessonProgress,Lesson
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddTeacherForm
from .models import TeacherProfile


def student_register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Student account created successfully."
            )

            return redirect("student_dashboard")
    else:
        form = StudentRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
            "registration_type": "Student"
        }
    )


def teacher_register(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Teacher account created successfully."
            )

            return redirect("teacher_dashboard")
    else:
        form = TeacherRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
            "registration_type": "Teacher"
        }
    )



from courses.models import Course, Enrollment
from django.utils.http import urlencode
from courses.models import Course, Enrollment
from django.urls import reverse

def home(request):
    courses = list(
        Course.objects.filter(is_published=True).order_by("-created_at")
    )

    enrolled_course_ids = set()

    if request.user.is_authenticated and hasattr(request.user, "student_profile"):
        enrolled_course_ids = set(
            Enrollment.objects.filter(
                student=request.user
            ).values_list("course_id", flat=True)
        )

    for course in courses:
        if request.user.is_authenticated and hasattr(request.user, "student_profile"):
            if course.id in enrolled_course_ids:
                course.home_url = reverse("student_course", args=[course.id])
                course.home_label = "Continue Learning"
            else:
                course.home_url = reverse("course_details", args=[course.id])
                course.home_label = "View Course"
        else:
            course.home_url = (
                reverse("login")
                + "?"
                + urlencode({
                    "next": reverse("course_details", args=[course.id])
                })
            )
            course.home_label = "Login to View"

    return render(request, "home.html", {"courses": courses})




@login_required
def student_dashboard(request):

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related("course")

    enrolled_courses_count = enrollments.count()

    completed_courses_count = 0
    in_progress_courses_count = 0

    for enrollment in enrollments:

        total_lessons = Lesson.objects.filter(
            module__course=enrollment.course
        ).count()

        completed_lessons = LessonProgress.objects.filter(
            student=request.user,
            lesson__module__course=enrollment.course,
            is_completed=True
        ).count()

        if total_lessons > 0 and completed_lessons == total_lessons:
            completed_courses_count += 1

        elif completed_lessons > 0:
            in_progress_courses_count += 1

    return render(
        request,
        "student/dashboard.html",
        {
            "enrolled_courses_count": enrolled_courses_count,
            "completed_courses_count": completed_courses_count,
            "in_progress_courses_count": in_progress_courses_count,
        }
    )

@login_required
def teacher_dashboard(request):

    courses = Course.objects.filter(
        teacher=request.user
    )

    total_courses = courses.count()

    published_courses = courses.filter(
        is_published=True
    ).count()

    return render(
        request,
        "teacher/dashboard.html",
        {
            "total_courses": total_courses,
            "published_courses": published_courses,
        }
    )


def user_logout(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")
def login_role(request):
    if request.method == "POST":
        role = request.POST.get("role")

        if role in ["student", "teacher"]:
            request.session["login_role"] = role
            return redirect("login_form")

    return render(
        request,
        "accounts/login_role.html"
    )



def user_login(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "student_profile"):
            return redirect("student_dashboard")

        if hasattr(request.user, "teacher_profile"):
            return redirect("teacher_dashboard")

        if request.user.is_staff:
            return redirect("/admin/")

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if hasattr(user, "student_profile"):
                return redirect("student_dashboard")

            if hasattr(user, "teacher_profile"):
                return redirect("teacher_dashboard")

            if user.is_staff:
                return redirect("/admin/")

            messages.error(
                request,
                "Your account does not have a valid role."
            )
            logout(request)

        else:
            messages.error(
                request,
                "Invalid username or password."
            )
    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )

@login_required
def change_password(request):

    if request.method == "POST":

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(old_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect("change_password")

        if len(new_password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters."
            )
            return redirect("change_password")

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(
            request,
            "Password changed successfully."
        )

    if hasattr(request.user, "student_profile"):
     return redirect("student_dashboard")

    if hasattr(request.user, "teacher_profile"):
     return redirect("teacher_dashboard")

     return redirect("home")
    return render(
        request,
        "accounts/change_password.html"
    )


@login_required
def add_teacher(request):
    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    if not request.user.teacher_profile.can_add_teacher:
        return redirect("teacher_dashboard")

    form = AddTeacherForm()

    if request.method == "POST":
        form = AddTeacherForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )

            TeacherProfile.objects.create(
                user=user,
                phone=form.cleaned_data["phone"],
                can_add_teacher=form.cleaned_data["can_add_teacher"],
            )

            messages.success(
                request,
                "Teacher created successfully!"
            )
            return redirect("teacher_dashboard")

    return render(
        request,
        "accounts/add_teacher.html",
        {"form": form},
    )
