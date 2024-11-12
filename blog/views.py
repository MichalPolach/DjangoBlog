from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.db.models import Count

def post_list(request, year=None, month=None):
    # This function remains the same
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    if year:
        posts = posts.filter(published_date__year=year)
    if month:
        posts = posts.filter(published_date__month=month)
    
    years = Post.objects.dates('published_date', 'year', order='DESC')
    months = Post.objects.dates('published_date', 'month', order='DESC')

    context = {
        'posts': posts,
        'year': year,
        'month': month,
        'years': years,
        'months': months,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):  # Changed from pk to slug
    post = get_object_or_404(Post, slug=slug)  # Changed from pk to slug
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)  # Changed from pk to slug
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):  # Changed from pk to slug
    post = get_object_or_404(Post, slug=slug)  # Changed from pk to slug
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)  # Changed from pk to slug
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})