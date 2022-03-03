from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'sample_input',
                  'sample_output', 'explanation', 'date_posted', 'tag', 'author')
