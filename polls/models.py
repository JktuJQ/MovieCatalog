from django.db import models
from django.contrib.auth.forms import User

from films.models import MyModel, Film


class Poll(MyModel):
    theme = models.CharField("Тема опроса", max_length=1024)
    description = models.TextField("Описание", blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор опроса")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="Фильм")

    class Meta:
        ordering = ["theme"]
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.theme


class Question(MyModel):
    question_types = (
    ("Один вариант ответа", "Один вариант ответа"), ("Несколько вариантов ответа", "Несколько вариантов ответа"))

    name = models.CharField("Вопрос", max_length=1024)
    question_type = models.CharField("Тип вопроса", max_length=30, choices=question_types, default=question_types[0])

    position = models.PositiveIntegerField("Позиция вопроса")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')

    class Meta:
        ordering = ["position", "pk"]
        verbose_name = 'Вопрос для голосования'
        verbose_name_plural = 'Вопросы для голосования'

    def __str__(self):
        return f'{self.name}'


class Choice(MyModel):
    name = models.CharField(max_length=200, verbose_name="Вариант ответа")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    votes = models.ManyToManyField(User, verbose_name="Проголосовавшие", blank=True)

    position = models.PositiveIntegerField("Позиция варианта ответа")

    class Meta:
        ordering = ["position", "pk"]
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return self.name
