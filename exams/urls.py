from django.urls import path
from . import views

urlpatterns = [
        path(
        "create/",
        views.create_exam,
        name="create_exam"
    ),
    path(
    "question/add/<int:exam_id>/",
    views.add_question,
    name="add_question"
),
path(
    "publish/<int:exam_id>/",
    views.publish_exam,
    name="publish_exam"
),
path(
    "student/<int:exam_id>/",
    views.student_exam,
    name="student_exam"
),
path(
    "student/",
    views.student_exams,
    name="student_exams"
),
]