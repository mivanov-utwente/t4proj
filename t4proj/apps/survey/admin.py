from django.contrib import admin
from .models import Question, Survey, Room


class RoomAdmin(admin.ModelAdmin):
    fields = ['name']


class QuestionAdmin(admin.ModelAdmin):
    fields = ['survey', 'question_text',
              'question_type', 'question_options']


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('text', 'question_type', 'choices')
    extra = 3


class SurveyAdmin(admin.ModelAdmin):
    fields = ['name', 'active']
    inlines = [QuestionInline]


#admin.site.register(Question, QuestionAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Survey, SurveyAdmin)
