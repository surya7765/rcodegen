from django.urls import path, include
from . import views
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView


urlpatterns = [
    path('', PostListView.as_view(), name="blog-home"),
    path('level/hard/', views.level_hard, name="level-hard"),
    path('level/medium/', views.level_medium, name="level-medium"),
    path('level/easy/', views.level_easy, name="level-easy"),
    path('level/misc/', views.level_misc, name="level-misc"),
    path('user/<str:id>/', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('post/pdf/<int:pk>/', views.post_render_pdf_view, name="blog-pdf"),
    path('about/', views.about, name='blog-about'),
    path('runcode/', views.runcode, name="runcode"),
]
