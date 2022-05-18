from django.db import models
from django.contrib.auth.models import User


class Vote(models.Model):
    title = models.CharField(max_length=50, verbose_name='Опрос')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Открытие опроса')
    published_of = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Закрытие опроса')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Опросы'
        verbose_name = 'Опрос'
        ordering = ['-published']


class Question(models.Model):
    vote = models.ForeignKey('Vote', null=True, on_delete=models.CASCADE, verbose_name='Опрос')
    TYPE = (
        ('text', 'Ввод ответа текстом'),
        ('one_choice', 'Ответ с выбором одного варианта'),
        ('some_choices', 'Ответ с выбором нескольких вариантов'),
    )
    name = models.CharField(max_length=50, choices=TYPE, verbose_name='Вопрос')
    correct_answer = models.CharField(max_length=50, verbose_name='Правильный ответ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = 'Вопрос'
        ordering = ['name']


class Variant(models.Model):
    question = models.ForeignKey('Question', null=True, on_delete=models.PROTECT, verbose_name='Вопрос')
    name_variant = models.CharField(max_length=50, verbose_name='Вариант')

    def __str__(self):
        return self.name_variant

    class Meta:
        verbose_name_plural = 'Варианты'
        verbose_name = 'Вариант'
        ordering = ['name_variant']


class Answer(models.Model):
    answer = models.IntegerField(verbose_name='Ответ')
    question = models.ForeignKey('Question', null=True, on_delete=models.PROTECT, verbose_name='Вопрос')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer", verbose_name='Пользователь')

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name_plural = 'Ответы'
        verbose_name = 'Ответ'
        ordering = ['answer']

