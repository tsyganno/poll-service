from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from app_poll.models import Answer


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer

        fields = ('answer',)

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset(
                'answer',
            ),
            ButtonHolder(Submit('submit', 'Перейти к выбору опросов'))
        )
