from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django import forms
import requests
from django.contrib.auth.models import User
from django.db import IntegrityError
from app_poll.forms import AnswerForm
from django.urls import reverse_lazy

from app_poll.models import Vote, Question, Variant, Answer


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


class QuestionView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'app_poll/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(vote__id=self.kwargs['pk'])
        context['vote'] = Vote.objects.get(id=self.kwargs['pk'])
        return context


class VoteView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'app_poll/votes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['votes'] = Vote.objects.all()
        return context


class IndexView(TemplateView):
    template_name = 'app_poll/index.html'


class TextAnswerView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:login'
    template_name = 'app_poll/text.html'
    form_class = AnswerForm
    model = Answer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = Variant.objects.filter(question__id=self.kwargs['pk'])
        context['question'] = Question.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question = Question.objects.get(id=self.kwargs['pk'])
        return super(TextAnswerView, self).form_valid(form)

    def get_success_url(self):
        question = Question.objects.get(id=self.kwargs['pk'])
        return reverse('poll:question', kwargs={'pk': question.pk})


class VariantView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'app_poll/variants.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = Variant.objects.filter(question__id=self.kwargs['pk'])
        context['question'] = Question.objects.get(id=self.kwargs['pk'])
        return context


def proba(request, pk: int):
    answer = Answer()
    num = Vote.objects.filter(question__id=pk).first().id
    variants = Variant.objects.filter(question__id=pk)
    if request.POST:
        for el in variants:
            if el.id == int(request.POST['variant']):
                answer.answer = el.name_variant
                answer.user = request.user
                answer.question = Question.objects.get(id=pk)
                answer.save()
    return HttpResponseRedirect(reverse('poll:question', args=[num]))
