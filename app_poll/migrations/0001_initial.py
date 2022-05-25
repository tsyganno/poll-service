# Generated by Django 4.0.4 on 2022-05-23 06:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_question', models.CharField(choices=[('text', 'Ответ вводом текста'),
                                                            ('one_choice', 'Ответ с выбором одного варианта'),
                                                            ('some_choices', 'Ответ с выбором нескольких вариантов')],
                                                   max_length=50, verbose_name='Тип вопроса')),
                ('text', models.CharField(max_length=100, verbose_name='Вопрос')),
                ('correct_answer', models.CharField(max_length=50, verbose_name='Правильный ответ')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['text'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Опрос')),
                ('published', models.DateTimeField(db_index=True, verbose_name='Открытие опроса')),
                ('published_off', models.DateTimeField(db_index=True, verbose_name='Закрытие опроса')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
                'ordering': ['-published'],
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_variant', models.CharField(max_length=50, verbose_name='Вариант')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                               to='app_poll.question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Вариант',
                'verbose_name_plural': 'Варианты',
                'ordering': ['name_variant'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='vote',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_poll.vote',
                                    verbose_name='Опрос'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=50, verbose_name='Ответ пользователя')),
                ('date_of_answer', models.DateTimeField(auto_now=True, db_index=True,
                                                        verbose_name='Дата и время ответа')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                               to='app_poll.question', verbose_name='Вопрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer',
                                           to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
                'ordering': ['answer'],
            },
        ),
    ]
