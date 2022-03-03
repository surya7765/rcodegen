from django.urls import path, include
from . import views
from polls.views import *

urlpatterns = [
    path('', QuestionListView.as_view(), name='polls-index'),
    path('<int:pk>/', QuestionDetailView.as_view(), name="polls-detail"),
    path('<int:question_id>/results/', views.results, name="polls-results"),
    path('<int:question_id>/vote/', views.vote, name="polls-vote"),
    path('user/<str:username>/', UserQuestionListView.as_view(), name="user-polls"),
    path('resultdata/<int:question_id>/', views.resultData, name="resultdata"),
    path('<int:pk>/delete/', QuestionDeleteView.as_view(), name="post-delete"),
    path('new/', QuestionChoiceCreateView.as_view(), name="polls-create"),
]
