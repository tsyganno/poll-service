from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.views.generic.base import TemplateView


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


class IndexView(TemplateView):
    template_name = 'app_poll/index.html'
