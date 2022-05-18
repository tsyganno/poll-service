from django.db import models


class Vote(models.Model):
    title = models.CharField(max_length=50, verbose_name='Опрос')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Опросы'
        verbose_name = 'Опрос'
        ordering = ['-published']


class QuestionType(models.Model):
    vote = models.ForeignKey('Vote', null=True, on_delete=models.CASCADE, verbose_name='Опрос')
    TYPE = (
        ('text', 'Ввод ответа текстом'),
        ('one_choice', 'Ответ с выбором одного варианта'),
        ('some_choices', 'Ответ с выбором нескольких вариантов'),
    )
    name = models.CharField(max_length=50, choices=TYPE, verbose_name='Вопрос')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = 'Вопрос'
        ordering = ['name']
