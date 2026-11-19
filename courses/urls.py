from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_course, name="create_course"),
    path("teacher/", views.teacher_courses, name="teacher_courses"),
    path("edit/<int:id>/", views.edit_course, name="edit_course"),
    path(
    "delete/<int:id>/",
    views.delete_course,
    name="delete_course"),
    path(
    "module/create/<int:course_id>/",
    views.create_module,
    name="create_module"),
    path(
    "module/edit/<int:module_id>/",
    views.edit_module,
    name="edit_module"),
    path(
    "module/delete/<int:module_id>/",
    views.delete_module,
    name="delete_module"),
    path(
    "student/courses/",
    views.student_courses,
    name="student_courses"),
    path(
    "student/courses/<int:id>/",
    views.course_details,
    name="course_details"),
    path(
    "student/courses/<int:id>/enroll/",
    views.enroll_course,
    name="enroll_course"),
    path(
    "student/my-courses/",
    views.student_enrolled_courses,
    name="student_enrolled_courses"),
    path(
    "student/my-courses/<int:id>/",
    views.student_course,
    name="student_course"),
    path(
    "lesson/create/<int:module_id>/",
    views.create_lesson,
    name="create_lesson"),
    path(
    "student/module/<int:module_id>/",
    views.student_module,
    name="student_module"
),
path(
    "lesson/edit/<int:lesson_id>/",
    views.edit_lesson,
    name="edit_lesson"
),

path(
    "lesson/delete/<int:lesson_id>/",
    views.delete_lesson,
    name="delete_lesson"
),
path(
    "lesson/complete/<int:lesson_id>/",
    views.complete_lesson,
    name="complete_lesson"
),
path("search/", views.global_search, name="global_search"),


]