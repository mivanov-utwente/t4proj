# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Survey, Room
from .forms import ResponseForm


def index(request):
    """
    Index view lists all available rooms for survey
    """
    rooms = Room.objects.order_by('name').all()
    return render(request, 'survey/index.html', context={'rooms': rooms})


def survey(request, room_slug):
    """
    Index view lists all available rooms for survey
    """
    room = get_object_or_404(Room, slug=room_slug)
    survey = get_object_or_404(Survey, active=True)
    form_initial = {'room': room, 'survey': survey}

    if request.method == 'POST':
        form = ResponseForm(request.POST, initial=form_initial)
        if form.is_valid():
            form.save(True)
            return HttpResponseRedirect(reverse('survey:thanks',
                                                args=(room_slug, )))
    else:
        form = ResponseForm(initial=form_initial)

    return render(request, 'survey/survey-mobile.html', context={
        'room': room,
        'form': form,
        'survey': survey,
    })


def thanks(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)
    return render(request, 'survey/thanks.html', context={'room': room})


