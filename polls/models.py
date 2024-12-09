from django.db import models
from django.contrib.auth.forms import User
import datetime

from films.models import MyModel, Person, Film


class Poll(MyModel):
    name = models.CharField("Тема", max_length=1024)
    description = models.TextField("Описание", blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор опроса")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="Фильм")

    def user_voted(self, user):
        user_votes = user.vote_set.all()
        done = user_votes.filter(poll=self)
        if done.exists():
            return False
        return True

    class Meta:
        ordering = ["name"]
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосования'

    def __str__(self):
        return f'{self.poll.theme}'


class Choice(MyModel):
    name = models.CharField(max_length=200, verbose_name="Вариант")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name="Опрос")
    votes = models.IntegerField(default=0, verbose_name="Кол-во голосов")

    class Meta:
        ordering = ["name"]
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'

    def __str__(self):
        return self.name


class Vote(MyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Голосующий")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name="Вариант")

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'

    def __str__(self):
        return f'{self.poll.theme} - {self.choice.name} - {self.user.username}'
