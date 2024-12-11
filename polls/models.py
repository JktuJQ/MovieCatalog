from django.db import models
from django.contrib.auth.forms import User

from films.models import MyModel, Film


class Question(MyModel):
    name = models.CharField("Вопрос", max_length=1024)

    class Meta:
        ordering = ["name"]
        verbose_name = 'Вопрос для голосования'
        verbose_name_plural = 'Вопросы для голосования'

    def __str__(self):
        return f'{self.name}'


class Choice(MyModel):
    name = models.CharField(max_length=200, verbose_name="Вариант ответа")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    votes = models.ManyToManyField(User, verbose_name="Проголосовавшие")

    class Meta:
        ordering = ["name"]
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return self.name


class Poll(MyModel):
    theme = models.CharField("Тема опроса", max_length=1024)
    description = models.TextField("Описание", blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор опроса")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="Фильм")

    polls = models.ManyToManyField(Question, verbose_name="Опросы")

    class Meta:
        ordering = ["theme"]
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.theme