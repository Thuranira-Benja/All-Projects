from django.shortcuts import render
from .models import Post

def blog_view(request):
    posts = Post.objects.filter(is_published=True)
    context = {
        'posts': posts,
    }
    return render(request, 'blog/blog.html', context)
