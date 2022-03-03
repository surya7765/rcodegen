from django.shortcuts import redirect, render, get_object_or_404
from blog.models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def level_hard(request):
    context = {
        'posts': Post.objects.filter(tag='hard')
    }
    return render(request, 'blog/home.html', context)


def level_medium(request):
    context = {
        'posts': Post.objects.filter(tag='medium')
    }
    return render(request, 'blog/home.html', context)


def level_easy(request):
    context = {
        'posts': Post.objects.filter(tag='easy')
    }

    return render(request, 'blog/home.html', context)


def level_misc(request):
    context = {
        'posts': Post.objects.filter(tag='misc')
    }

    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # print(user)
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body', 'sample_input',
              'sample_output', 'explanation', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body', 'sample_input',
              'sample_output', 'explanation', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def post_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    post = get_object_or_404(Post, pk=pk)
    template_path = 'blog/pdf_view.html'
    context = {'post': post}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def quiz(request):
    return HttpResponse('<h1>Quiz</h1>')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
