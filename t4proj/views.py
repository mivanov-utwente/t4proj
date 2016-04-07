# -*- coding: utf-8 -*-
from django.shortcuts import render


def home(request):
    return render(request, 'index.html', context={})


def handler_404(request):
    return render(request, 'errors/404.html', context={})


def handler_500(request):
    return render(request, 'errors/500.html', context={})

