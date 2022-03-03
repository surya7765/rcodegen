from django.forms import ModelForm, inlineformset_factory
from polls.models import Question, Choice


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ()


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        exclude = ()

ChoiceFormSet = inlineformset_factory(Question, Choice,
                                        form=ChoiceForm, extra=1)
