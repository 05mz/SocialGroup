from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import request

from .models import Post, Comment

# Create your views here.


def list_posts(request):
    # Limit to 10 latest posts
    posts = Post.objects.all().order_by('-created_at')[:10]
    return render(request, 'social/list.html', {'posts': posts})


from .forms import CommentForm


def post_detailview(request, id):


    if request.method == 'POST':
        cf = CommentForm(request.POST or None)
        if cf.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post=Post, user=request.user, content=content)
            comment.save()
            return redirect(Post.get_absolute_url())
        else:
            cf = CommentForm()

        context = {
            'comment_form': cf,
        }
        return render(request, 'social/post_detail.html', context)
