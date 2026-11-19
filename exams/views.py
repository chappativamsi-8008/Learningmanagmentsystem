from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Exam, Question, ExamAttempt
from .forms import ExamForm, QuestionForm
from courses.models import Course
from .models import Question
from django.shortcuts import get_object_or_404
from progress.models import CourseProgress
from certificates.models import Certificate
import uuid
from courses.models import LessonProgress
@login_required
def create_exam(request):

    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    courses = Course.objects.filter(
        teacher=request.user
    )

    if request.method == "POST":

        form = ExamForm(request.POST)

        if form.is_valid():

            exam = form.save(commit=False)

            if exam.course.teacher != request.user:
                return redirect("teacher_dashboard")

            exam.save()

            return redirect("add_question",exam_id=exam.id)

    else:
        form = ExamForm()

    form.fields["course"].queryset = courses

    return render(
        request,
        "exams/create_exam.html",
        {
            "form": form
        }
    )
@login_required
def add_question(request, exam_id):

    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id,
        course__teacher=request.user
    )

    if request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()

            return redirect(
                "add_question",
                exam_id=exam.id
            )

    else:
        form = QuestionForm()

    questions = exam.questions.all()

    return render(
        request,
        "exams/add_question.html",
        {
            "form": form,
            "exam": exam,
            "questions": questions,
        }
    )
@login_required
def publish_exam(request, exam_id):

    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id,
        course__teacher=request.user
    )

    if exam.questions.count() == 0:
        return redirect(
            "add_question",
            exam_id=exam.id
        )

    exam.is_published = True
    exam.save()

    return redirect(
        "add_question",
        exam_id=exam.id
    )

@login_required
def student_exams(request):
    if not hasattr(request.user, "student_profile"):
        return redirect("home")

    exams = Exam.objects.filter(is_published=True)

    return render(
        request,
        "exams/student_exams.html",
        {"exams": exams}
    )
  
@login_required
def student_exam(request, exam_id):

    if not hasattr(request.user, "student_profile"):
        return redirect("home")

    exam = get_object_or_404(
        Exam,
        id=exam_id,
        is_published=True
    )

    progress = CourseProgress.objects.filter(
        student=request.user,
        course=exam.course
    ).first()

    if not progress or progress.progress_percentage < 100:
        return redirect(
            "student_course",
            id=exam.course.id
        )

    questions = exam.questions.all()

    if request.method == "POST":

        total_marks = 0
        obtained_marks = 0

        for question in questions:

            total_marks += question.marks

            answer = request.POST.get(
                f"question_{question.id}"
            )

            if answer == question.correct_answer:
                obtained_marks += question.marks

        if total_marks > 0:
            percentage = (
                obtained_marks / total_marks
            ) * 100
        else:
            percentage = 0

        passed = percentage >= exam.pass_percentage

        ExamAttempt.objects.create(
            student=request.user,
            exam=exam,
            total_marks=total_marks,
            obtained_marks=obtained_marks,
            percentage=percentage,
            passed=passed,
        )
        certificate = None

        if passed:
            all_lessons_completed = not LessonProgress.objects.filter(
                student=request.user,
                lesson__module__course=exam.course,
                is_completed=False
            ).exists()

            if all_lessons_completed:
                certificate, created = Certificate.objects.get_or_create(
                    student=request.user,
                    course=exam.course,
                    defaults={
                        "certificate_id": str(uuid.uuid4())
                    }
                )
        return render(
            request,
            "exams/exam_result.html",
            {
                "exam": exam,
                "total_marks": total_marks,
                "obtained_marks": obtained_marks,
                "percentage": percentage,
                "passed": passed,
                "certificate": certificate,
            }
        )

    return render(
        request,
        "exams/student_exam.html",
        {
            "exam": exam,
            "questions": questions,
        }
    )