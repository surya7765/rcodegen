from django.urls import path, include
from . import views
from quiz.views import *

urlpatterns = [
    path('', home, name='quiz-index'),
]
