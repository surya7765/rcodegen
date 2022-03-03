from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.utils import timezone
from django.utils.timezone import now
from django.urls import reverse


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=now)
    qus_author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    
    def get_absolute_url(self):
        return reverse('polls-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
