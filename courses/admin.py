from django.contrib import admin
from .models import Course, Module, Enrollment, Lesson, LessonProgress

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(Lesson)
admin.site.register(LessonProgress)