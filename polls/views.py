from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Question, Choice
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from polls.forms import QuestionForm, ChoiceFormSet
from django.db import transaction
from django.urls import reverse_lazy


# Create your views here.


def home(request):
    context = {
        'questions': Question.objects.all()
    }
    return render(request, 'polls/index.html', context)


class QuestionListView(ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'questions'
    ordering = ['-pub_date']
    paginate_by = 10


class UserQuestionListView(ListView):
    model = Question
    template_name = 'polls/user_polls.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # print(user)
        return Question.objects.filter(qus_author=user).order_by('-pub_date')


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'polls/question_detail.html'


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


# Vote for a question choice
def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/question_detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls-results', args=(question.id,)))


def resultData(request, question_id):
    voteData = []
    question = Question.objects.get(pk=question_id)
    votes = question.choice_set.all()

    for i in votes:
        voteData.append({i.choice_text: i.votes})
    # print(voteData)
    return JsonResponse(voteData, safe=False)


class QuestionChoiceCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question_text']

    def get_context_data(self, **kwargs):
        data = super(QuestionChoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = ChoiceFormSet(self.request.POST)
        else:
            data['questions'] = ChoiceFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.qus_author = self.request.user
        questions = context['questions']
        with transaction.atomic():
            self.object = form.save()
            if questions.is_valid():
                questions.instance = self.object
                questions.save()
        
        return super(QuestionChoiceCreateView, self).form_valid(form)


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('polls-index')

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.qus_author:
            return True
        return False
