from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
def posts_list(request):
    return render(request, 'posts/posts_list.html', {'posts': Post.objects.all().order_by('-date')})

def post_page(request, slug):
    return render(request, 'posts/post_page.html', {'post': Post.objects.get(slug=slug)})

@login_required(login_url="/users/login/")
def post_new(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            # save post to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return render(request, 'posts/post_page.html', {'post': instance})
    else:
        form = forms.CreatePost()
    return render(request, 'posts/post_new.html', {'form': form})