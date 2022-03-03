from django.db import models
from django.db.models.base import Model
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.urls import reverse
# Create your models here.

LEVEL_CHOICES = (
    ('easy', 'EASY'),
    ('medium', 'MEDIUM'),
    ('hard', 'HARD'),
    ('misc', 'MISC'),
)

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = HTMLField(blank=True, null=True)
    sample_input = models.TextField(blank=True, null=True)
    sample_output = models.TextField(blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    tag = models.CharField(max_length=6, choices=LEVEL_CHOICES, default='easy')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
