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


class QuestionnaireForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuestionnaireForm, self).__init__(*args, **kwargs)

        for question in questions:
            choices = question.choice_set.all()
            if question.question_type == "Один вариант ответа":
                self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                    queryset=choices,
                    widget=forms.RadioSelect,
                    empty_label=None,
                    label=question.text,
                    required=True,
                )
            else:
                self.fields[f'question_{question.id}'] = forms.ModelMultipleChoiceField(
                    queryset=choices,
                    widget=forms.CheckboxSelectMultiple,
                    label=question.text,
                    required=False,
                )
                self.fields[f'question_{question.id}'].question = question

    def clean(self):
        cleaned_data = super().clean()
        for field_name, field in self.fields.items():
            if hasattr(field, 'question') and field.question.question_type != "Один вариант ответа":
                selected_choices = cleaned_data.get(field_name)
                if not selected_choices:
                    self.add_error(field_name, "Please select at least one option.")