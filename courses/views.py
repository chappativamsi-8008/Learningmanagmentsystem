from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404

from .forms import CourseForm, ModuleForm
from django.db.models import Q

from .models import Course, Module, Lesson
from .models import Enrollment, LessonProgress
from progress.models import CourseProgress
@login_required
def create_course(request):
    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()

            return redirect("teacher_dashboard")
    else:
        form = CourseForm()

    return render(
        request,
        "courses/create_course.html",
        {"form": form}
    )


@login_required
def teacher_courses(request):
    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    courses = Course.objects.filter(
        teacher=request.user
    )

    return render(
        request,
        "courses/teacher_courses.html",
        {"courses": courses}
    )



@login_required
def edit_course(request, id):
    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    course = Course.objects.get(
        id=id,
        teacher=request.user
    )

    if request.method == "POST":
        form = CourseForm(
            request.POST,
            request.FILES,
            instance=course
        )

        if form.is_valid():
            form.save()
            return redirect("teacher_courses")
    else:
        form = CourseForm(instance=course)

    return render(
        request,
        "courses/edit_course.html",
        {
            "form": form,
            "course": course
        }
    )


@login_required
def delete_course(request, id):
    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    course = Course.objects.get(
        id=id,
        teacher=request.user
    )

    if request.method == "POST":
        course.delete()
        return redirect("teacher_courses")

    return render(
        request,
        "courses/delete_course.html",
        {"course": course}
    )


@login_required
def create_module(request, course_id):
    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    course = Course.objects.get(
        id=course_id,
        teacher=request.user
    )

    if request.method == "POST":
        form = ModuleForm(request.POST)

        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()

            return redirect("teacher_courses")
    else:
        form = ModuleForm()

    return render(
        request,
        "courses/create_module.html",
        {
            "form": form,
            "course": course
        }
    )
@login_required
def edit_module(request, module_id):

    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    module = Module.objects.get(
        id=module_id,
        course__teacher=request.user
    )

    if request.method == "POST":

        form = ModuleForm(
            request.POST,
            instance=module
        )

        if form.is_valid():
            form.save()

            return redirect("teacher_courses")

    else:
        form = ModuleForm(instance=module)

    return render(
        request,
        "courses/edit_module.html",
        {
            "form": form,
            "module": module,
            "course": module.course,
        }
    )
@login_required
def delete_module(request, module_id):

    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    module = Module.objects.get(
        id=module_id,
        course__teacher=request.user
    )

    if request.method == "POST":
        course_id = module.course.id
        module.delete()

        return redirect("teacher_courses")

    return render(
        request,
        "courses/delete_module.html",
        {
            "module": module,
            "course": module.course,
        }
    )
@login_required
def student_courses(request):

    if not hasattr(request.user, "student_profile"):
        return redirect("home")

    courses = Course.objects.filter(
        is_published=True
    )

    return render(
        request,
        "courses/student_courses.html",
        {
            "courses": courses
        }
    )
@login_required
def student_course(request, id):
 if not hasattr(request.user, "student_profile"):
    return redirect("home")

    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course_id=id
    )

    course = enrollment.course

    total_lessons = Lesson.objects.filter(
        module__course=course
    ).count()

    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__module__course=course,
        is_completed=True
    ).count()

    if total_lessons > 0:
        progress_percentage = int(
            (completed_lessons / total_lessons) * 100
        )
    else:
        progress_percentage = 0
        remaining_lessons = total_lessons - completed_lessons

    return render(
        request,
        "courses/student_course.html",
        {
            "course": course,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "progress_percentage": progress_percentage,
            "remaining_lessons": remaining_lessons,
        }
    )
@login_required
def course_details(request, id):

    if not hasattr(request.user, "student_profile"):
        return redirect("home")

    course = Course.objects.get(id=id)

    return render(
        request,
        "courses/course_details.html",
        {
            "course": course
        }
    )
@login_required
def enroll_course(request, id):

    if not hasattr(request.user, "student_profile"):
        return redirect("home")

    course = get_object_or_404(Course, id=id)

    Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    return redirect("student_enrolled_courses")
@login_required
def student_enrolled_courses(request):

    if not hasattr(request.user, "student_profile"):
        return redirect("home")

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related("course")

    return render(
        request,
        "courses/student_enrolled_courses.html",
        {
            "enrollments": enrollments
        }
    )
@login_required
def student_course(request, id):

    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course_id=id
    )

    course = enrollment.course

    total_lessons = Lesson.objects.filter(
        module__course=course
    ).count()

    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__module__course=course,
        is_completed=True
    ).count()

    if total_lessons > 0:
        progress_percentage = int(
            (completed_lessons / total_lessons) * 100
        )
    else:
        progress_percentage = 0

    return render(
        request,
        "courses/student_course.html",
        {
            "course": course,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "progress_percentage": progress_percentage,
        }
    )


@login_required
def create_lesson(request, module_id):
    if not hasattr(request.user, "teacher_profile"):
        return redirect("home")

    module = get_object_or_404(
        Module,
        id=module_id,
        course__teacher=request.user
    )

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        matter_link = request.POST.get("matter_link")
        video_link = request.POST.get("video_link")
        order = request.POST.get("order")

        Lesson.objects.create(
            module=module,
            title=title,
            description=description,
            matter_link=matter_link,
            video_link=video_link,
            order=order
        )

        return redirect("teacher_courses")

    return render(
        request,
        "courses/create_lesson.html",
        {
            "module": module
        }
    )


@login_required
def student_module(request, module_id):
    if not hasattr(request.user, "student_profile"):
        return redirect("home")

    module = get_object_or_404(
        Module,
        id=module_id
    )

    # Student must be enrolled in this course
    get_object_or_404(
        Enrollment,
        student=request.user,
        course=module.course
    )

    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__module=module,
        is_completed=True
    ).values_list(
        "lesson_id",
        flat=True
    )

    return render(
        request,
        "courses/student_module.html",
        {
            "module": module,
            "completed_lessons": completed_lessons,
        }
    )

@login_required
def student_module(request, module_id):

    if not hasattr(request.user, "student_profile"):
        return redirect("home")

    module = get_object_or_404(
        Module,
        id=module_id
    )

    # Student must be enrolled in this course
    get_object_or_404(
        Enrollment,
        student=request.user,
        course=module.course
    )

    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__module=module,
        is_completed=True
    ).values_list(
        "lesson_id",
        flat=True
    )

    return render(
        request,
        "courses/student_module.html",
        {
            "module": module,
            "completed_lessons": completed_lessons,
        }
    )
@login_required
def complete_lesson(request, lesson_id):
 if not hasattr(request.user, "student_profile"):
    return redirect("home")

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id
    )

    get_object_or_404(
        Enrollment,
        student=request.user,
        course=lesson.module.course
    )

    LessonProgress.objects.update_or_create(
        student=request.user,
        lesson=lesson,
        defaults={
            "is_completed": True
        }
    )

    course = lesson.module.course

    total_lessons = Lesson.objects.filter(
        module__course=course
    ).count()

    completed_lessons = LessonProgress.objects.filter(
        student=request.user,
        lesson__module__course=course,
        is_completed=True
    ).count()

    if total_lessons > 0:
        progress_percentage = (
            completed_lessons / total_lessons
        ) * 100
    else:
        progress_percentage = 0

    CourseProgress.objects.update_or_create(
        student=request.user,
        course=course,
        defaults={
            "progress_percentage": progress_percentage
        }
    )

    return redirect(
        "student_module",
        module_id=lesson.module.id
    )
@login_required
def edit_lesson(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        module__course__teacher=request.user
    )

    if request.method == "POST":

        lesson.title = request.POST.get("title")
        lesson.description = request.POST.get("description")
        lesson.matter_link = request.POST.get("matter_link")
        lesson.video_link = request.POST.get("video_link")
        lesson.order = request.POST.get("order")

        lesson.save()

        return redirect("teacher_courses")

    return render(
        request,
        "courses/edit_lesson.html",
        {
            "lesson": lesson,
            "module": lesson.module
        }
    )
@login_required
def delete_lesson(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        module__course__teacher=request.user
    )

    if request.method == "POST":

        lesson.delete()

        return redirect("teacher_courses")

    return render(
        request,
        "courses/delete_lesson.html",
        {
            "lesson": lesson,
            "module": lesson.module
        }
    )

def global_search(request):
    query = request.GET.get("q", "").strip()
    courses = Course.objects.none()

    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query),
            is_published=True
        )

    return render(
        request,
        "courses/search_results.html",
        {
            "query": query,
            "courses": courses,
        }
    )
