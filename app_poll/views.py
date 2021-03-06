from datetime import datetime
from django.shortcuts import reverse
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from app_poll.forms import AnswerForm

from app_poll.models import Vote, Question, Variant, Answer


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


class QuestionByTypeView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'app_poll/question_by_type.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(type_question=self.kwargs['type'], vote__id=self.kwargs['pk'])
        context['vote'] = Vote.objects.get(id=self.kwargs['pk'])
        context['type'] = Question.objects.filter(type_question=self.kwargs['type']).first()
        return context


class QuestionView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'app_poll/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_question_set = set()
        for el in Question.objects.filter(vote__id=self.kwargs['pk']):
            type_question_set.add(el.type_question)
        context['types'] = type_question_set
        context['vote'] = Vote.objects.get(id=self.kwargs['pk'])
        return context


class VoteView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'app_poll/votes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        time_now = datetime.now()
        context['votes'] = Vote.objects.filter(published_off__gt=time_now, published__lt=time_now)
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
        num = Question.objects.get(id=self.kwargs['pk']).id
        vote_pk = Vote.objects.filter(question__id=num).first().id
        return reverse('poll:question', kwargs={'pk': vote_pk})


class VariantView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'app_poll/variants.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = Variant.objects.filter(question__id=self.kwargs['pk'])
        context['question'] = Question.objects.get(id=self.kwargs['pk'])
        return context


class SomeVariantView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'app_poll/some_variants.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = Variant.objects.filter(question__id=self.kwargs['pk'])
        context['question'] = Question.objects.get(id=self.kwargs['pk'])
        return context


def record_to_model_one_answer(request, pk: int):
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


def record_to_model_some_answers(request, pk: int):
    answer = Answer()
    num = Vote.objects.filter(question__id=pk).first().id
    variants = Variant.objects.filter(question__id=pk)
    id_list = request.POST.getlist('variantid')
    answer_word = ''
    if request.POST:
        for variant in variants:
            for el in id_list:
                if variant.id == int(el):
                    answer_word += str(variant.name_variant) + ' '
        answer.answer = answer_word
        answer.user = request.user
        answer.question = Question.objects.get(id=pk)
        answer.save()
    return HttpResponseRedirect(reverse('poll:question', args=[num]))


class OutcomeView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'app_poll/outcome.html'

    def get(self, request, *args, **kwargs):
        answers_user = Answer.objects.filter(user__id=self.kwargs['pk'])
        questions_answers = {}
        count = 0
        for answer in answers_user:
            key = f'{answer.question.text} Дата и время попытки: ' \
                  f'{str(answer.date_of_answer)[:str(answer.date_of_answer).find(".")]}.'
            if answer.question.type_question != 'some_choices':
                if str(answer.question.correct_answer).lower() == str(answer.answer).lower():
                    count += 1
                    questions_answers[key] = f'Правилный ответ: {str(answer.question.correct_answer)}, ' \
                                             f'а ваш ответ: {str(answer.answer)}. ' \
                                             f'Вы ответили правильно и получаете: +1 балл.'
                else:
                    questions_answers[key] = f'Правилный ответ: {str(answer.question.correct_answer)}, ' \
                                             f'а ваш ответ: {str(answer.answer)}. Вы ответили неправильно.'
            else:
                counter = 0
                question_list = list(map(lambda x: x.lower(), str(answer.question.correct_answer).split()))
                answer_list = list(map(lambda x: x.lower(), str(answer.answer).split()))
                for el in answer_list:
                    if el in question_list:
                        counter += 1
                if counter == len(question_list):
                    count += 1
                    questions_answers[key] = f'Правилный ответ: {str(answer.question.correct_answer)}, ' \
                                             f'а ваш ответ: {str(answer.answer)}. ' \
                                             f'Вы ответили правильно и получаете: +1 балл.'
                else:
                    questions_answers[key] = f'Правилный ответ: {str(answer.question.correct_answer)}, ' \
                                             f'а ваш ответ: {str(answer.answer)}. Вы ответили неправильно.'
        return self.render_to_response({'dict': questions_answers, 'count': count, 'count_2': len(answers_user)})


class DeleteAnswerView(LoginRequiredMixin, DeleteView):
    login_url = 'accounts:login'
    template_name = 'app_poll/delete_answer.html'
    model = Answer

    def get_queryset(self):
        owner = self.request.user.pk
        return self.model.objects.filter(user__id=owner)

    def get_object(self, queryset=None):
        return self.get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['answers'] = Answer.objects.filter(user__id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('poll:vote')
