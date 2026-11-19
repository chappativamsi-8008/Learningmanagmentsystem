 
from django import forms
from .models import Course, Module


class ModuleForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = [
            "title",
            "description",
            "order",
        ]

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            "title",
            "description",
            "thumbnail",
            "price",
            "is_published",
        ]

