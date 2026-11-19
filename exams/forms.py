from django import forms
from .models import Exam
from .models import Question


class ExamForm(forms.ModelForm):

    class Meta:
        model = Exam
        fields = [
            "course",
            "title",
            "instructions",
            "pass_percentage",
            "is_published",
        ]

        widgets = {
            "instructions": forms.Textarea(
                attrs={"rows": 4}
            ),
            "pass_percentage": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 100
                }
            ),
        }


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = [
            "question_text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_answer",
            "marks",
        ]

        widgets = {
            "question_text": forms.Textarea(
                attrs={"rows": 3}
            ),
        }