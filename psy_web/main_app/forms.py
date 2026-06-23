from django import forms
from .models import Question


class TestForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for q in questions:
            if q.question_type == 'single':
                choices = [(opt.id, opt.text) for opt in q.options.all()]
                self.fields[f'question_{q.id}'] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect,
                    label=q.text,
                    required=True
                )
            elif q.question_type == 'multiple':
                choices = [(opt.id, opt.text) for opt in q.options.all()]
                self.fields[f'question_{q.id}'] = forms.MultipleChoiceField(
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple,
                    label=q.text,
                    required=True
                )
            elif q.question_type == 'scale':
                self.fields[f'question_{q.id}'] = forms.IntegerField(
                    label=q.text,
                    min_value=0,
                    max_value=10,  # при необходимости можно сделать настраиваемым
                    required=True
                )
            elif q.question_type == 'text':
                self.fields[f'question_{q.id}'] = forms.CharField(
                    label=q.text,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    required=True,
                    max_length=255
                )
