from django import forms
from .models import Poll, Question, Choice
from django.forms import formset_factory, modelformset_factory, BaseModelFormSet


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
                    required=True,
                )

    def clean(self):
        cleaned_data = super().clean()
        for field_name, field in self.fields.items():
            if field.required:
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, "Сделайте выбор")


ChoiceFormSet = formset_factory(ChoiceForm, extra=0, min_num=2, validate_min=True)


class ChoiceUpdateFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['DELETE'] = forms.BooleanField(required=False, label="Удалить")
