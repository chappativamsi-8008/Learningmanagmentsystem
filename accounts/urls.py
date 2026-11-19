from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),
    path(
        "register/student/",
        views.student_register,
        name="student_register"
    ),
 path(
    "login/",
    views.user_login,
    name="login"
),

    path(
        "login/form/",
        views.user_login,
        name="login_form"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "student/dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    path(
        "teacher/dashboard/",
        views.teacher_dashboard,
        name="teacher_dashboard"
    ),
    path(
    "change-password/",
    views.change_password,
    name="change_password"
),
path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"
    ),
    name="password_reset"
),

path(
    "password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ),
    name="password_reset_done"
),

path(
    "password-reset-confirm/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"
    ),
    name="password_reset_confirm"
),

path(
    "password-reset-complete/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ),
    name="password_reset_complete"
),

path("add-teacher/", views.add_teacher, name="add_teacher"),

]