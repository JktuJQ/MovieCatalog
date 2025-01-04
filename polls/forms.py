from django import forms
from .models import Poll, Question, Choice
from django.forms import formset_factory


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'question_type', 'position']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['name', 'position']


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['theme', 'description']


QuestionFormSet = formset_factory(QuestionForm, min_num=1, validate_min=True)
ChoiceFormSet = formset_factory(ChoiceForm, min_num=2, validate_min=True)
