from .models import Post, Comment, User

# Create your views here.


def list_posts(request):
    # Limit to 10 latest posts
    posts = Post.objects.all().order_by('-created_at')[:10]
    return render(request, 'social/list.html', {'posts': posts})
