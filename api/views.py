from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import PostSerializer
from blog.models import Post
from rest_framework.response import Response
import random
from django.db.models import Max


def pick_random_object():
    # n =
    # print(Post.objects.latest('id').id)
    posts = Post.objects.values_list('id', flat=True)
    # print(list(posts))
    max_id = Post.objects.all().aggregate(max_id=Max("id"))['max_id']
    random_id = random.randrange(1, max_id + 1)
    # print(random_id)
    if random_id in posts:
        return random_id
    else:
        return pick_random_object()


class PostViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdminUser]
    serializer_class = PostSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Post.objects.all().filter(id=pick_random_object())
