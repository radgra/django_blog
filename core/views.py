from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from comments.forms import CommentAnonForm, CommentForm

# Create your views here.


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get("page", 1)

    categories = Category.objects.all()
    tags = Tag.objects.all()
    liked_posts = (
        Post.objects.all().annotate(likes_count=Count("like")).order_by("-likes_count")
    )
    featured_posts = Post.objects.filter(is_featured=True)
    context = {
        "posts": paginator.get_page(page),
        "categories": categories,
        "tags": tags,
        "liked_posts": liked_posts,
        "featured_posts": featured_posts,
    }
    return render(request, "core/index.html", context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    tags = Tag.objects.all()
    liked_posts = (
        Post.objects.all().annotate(likes_count=Count("like")).order_by("-likes_count")
    )
    categories = Category.objects.all()
    context = {
        "post": post,
        "categories": categories,
        "tags": tags,
        "liked_posts": liked_posts
    }

    if request.method == "POST":
        comment = request.POST.copy()
        comment['post'] = post.id
        if request.user:
            comment['user'] = request.user.id
        form = CommentForm(comment)
        if form.is_valid():
            # some logic
            form.save()
            return redirect('blog:post_detail', pk)
    else:
        form = CommentForm()

    context['form'] = form
    return render(request, "core/detail.html", context)

