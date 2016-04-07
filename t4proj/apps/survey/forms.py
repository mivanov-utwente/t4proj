# -*- coding: utf-8 -*-
import uuid
from django import forms
from django.utils.text import slugify

from .models import Answer, Question, Response
from .widgets import RatingRadioWidget


def _create_field(question_type, text, required=True, choices=None):
    fields = (None, None)
    if question_type == Question.TEXT:
        fields = (forms.CharField(label=text, required=False,
            widget=forms.Textarea), None)
    elif question_type == Question.CHOICE:
        radio = forms.ChoiceField(label=text, required=True,
            widget=forms.RadioSelect(), choices=choices)
        fields = (radio, None)
    elif question_type == Question.RATING:
        radio = forms.ChoiceField(label=text, required=True,
            widget=RatingRadioWidget(),
            choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],)
        fields = (radio, None)
    return fields


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = []

    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        if not 'room' in self.initial:
            raise ValueError('Missing room.')
        if not 'survey' in self.initial:
            raise ValueError('Missing survey form.')

        questions = self._get_survey_questions()
        for question in questions:
            key = 'question-%d' % (question.pk)
            fields = _create_field(question.question_type, question.text,
                required=True, choices=question.get_choices())
            self.fields[key] = fields[0]

    def _get_survey_questions(self):
        s = self.initial['survey']
        return s.questions.all()

    def save(self, commit=True):
        if 'room' in self.initial:
            self.instance.room = self.initial['room']
        if 'survey' in self.initial:
            self.instance.survey = self.initial['survey']
        self.instance.slug = slugify(uuid.uuid4().hex)
        response = super(ResponseForm, self).save(commit)

        questions = self._get_survey_questions()
        data = self.cleaned_data
        for idx, q in enumerate(questions):
            ans = Answer()
            ans.response = response
            ans.question = q
            ans.index = idx
            ans.body = data['question-{}'.format(q.pk)]
            ans.save()

        return response

