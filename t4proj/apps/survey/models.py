# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.utils.text import slugify


class Room(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Room, self).save(*args, **kwargs)


class Survey(models.Model):
    name = models.CharField(max_length=60)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    TEXT = 'T'
    RATING = 'R'
    CHOICE = 'C'

    QUESTION_TYPES = (
        (TEXT, 'Open Question'),
        (CHOICE, 'Multiple Choice'),
        (RATING, 'Rating'),
    )

    text = models.TextField(help_text="Enter your question here.")
    survey = models.ForeignKey(Survey, related_name='questions',
                                       on_delete=models.CASCADE)
    question_type = models.CharField(
        max_length=1, choices=QUESTION_TYPES, default=TEXT,
        help_text="Choose the type of answser.")

    choices = models.TextField(blank=True, null=True,
        help_text="Enter choices here separated by a new line.")

    def __str__(self):
        return self.text

    def get_choices(self):
        choices_list = []
        if self.choices:
            for choice in self.choices.split('\n'):
                choice = choice.strip()
                choices_list += [(choice, choice)]
        return choices_list


class ResponseManager(models.Manager):
    def create(self, **kwargs):
        return super(ResponseManager, self).create(
            slug=slugify(uuid.uuid4().hex), **kwargs)


class Response(models.Model):
    """
    Response to a Survey. A Response is composed of multiple Answers
    to Questions.
    """
    objects = ResponseManager()

    slug = models.SlugField()  # Unique id
    room = models.ForeignKey(Room, related_name='responses')
    survey = models.ForeignKey(Survey, null=True, related_name='responses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Room[{}]-{}'.format(self.room, self.slug)


class Answer(models.Model):
    """
    Answer as a part of a Response to a Survey.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.ForeignKey(Response, related_name='answers',
                                           on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers')
    index = models.IntegerField(help_text="Position in the response list.")
    body = models.TextField(blank=True, null=True)

    @property
    def text(self):
        return self.body

    def __str__(self):
        return self.body