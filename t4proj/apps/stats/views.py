from datetime import datetime, timedelta, time
from collections import OrderedDict
from operator import itemgetter, attrgetter

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect

from t4proj.apps.survey.models import Room, Survey, Response, Answer, Question
from django.db.models import Q

from . import forms, queries


# Create your views here.
def dashboard(request, room=None):
    return HttpResponseRedirect(reverse('stats:explore'))


def _build_explore_data_from_filter(filter_data):
    answers = quieries.answers_filtered_by_survey_rooms_daterange_timerange(
        filter_data['survey_id'], filter_data['room_ids'],
        filter_data['daterange'], filter_data['timerange'])

    questions = {a.question for a in answers}
    data = {}
    for q in questions:
        if q.question_type == q.RATING:
            results = OrderedDict((str(i), 0) for i in range(5, 0, -1))
        elif q.question_type == q.TEXT:
            results = []
        else:
            results = {}

        data[q] = {
            'id': q.id,
            'type': q.question_type,
            'text': q.text,
            'results': results,
        }

    for a in answers:
        q = a.question
        res = data[q]['results']
        if q.question_type == q.TEXT:
            if a.text is not None and len(a.text) > 0 and len(res) <= 10:
                res.append({'datetime': a.created_at, 'text': a.text})
        else:
            res[a.text] = res.get(a.text, 0) + 1

    for r in data.values():
        if r['type'] in [q.RATING, q.CHOICE]:
            r['total_votes'] = sum(_ for _ in r['results'].values())

    type_order = {Question.RATING: 1, Question.CHOICE: 2, Question.TEXT: 3}
    return OrderedDict(sorted(data.items(),
                       key=lambda t: type_order[t[0].question_type]))


def explore(request):
    active_survey = Survey.objects.get(active=True)
    rooms = Room.objects.order_by('name').all()
    surveys = Survey.objects.order_by('active', 'name').all()

    form_class = forms.data_filter_form_class_factory(
        [(r.id, r.name) for r in rooms], [(s.id, s.name) for s in surveys])

    data = {}
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            data = _build_explore_data_from_filter(form.cleaned_data)
    elif active_survey is not None:
        form = form_class(initial={'survey_id': str(active_survey.id)})
    else:
        form = form_class()

    return render(request, 'stats/explore.html', context={
        'form': form,
        'data': data,
        'rooms': rooms,
        'surveys': surveys,
    })


def log(request):
    page = request.GET.get('page', 1)
    per_page = max(1, int(request.GET.get('per_page', 20)))
    responses_all = Response.objects.order_by('created_at').all()
    paginator = Paginator(responses_all, per_page)

    try:
        responses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        responses = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        responses = paginator.page(paginator.num_pages)

    return render(request, 'stats/log.html', context={
        'responses': responses,
    })
