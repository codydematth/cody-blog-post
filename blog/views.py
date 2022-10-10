from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import *
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from operator import attrgetter
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Comment

POSTS_PER_PAGE = 5

def home(request):
        posts = Post.objects.all()
        posts = sorted(Post.objects.all(), key=attrgetter('date_posted'), reverse=True)
        #Search
        query = request.GET.get('q')
        if query:
            posts = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username=query)
                ).distinct()
         
        context = {
            'posts': posts,
        }
          
        # Pagination
        page = request.GET.get('page', 1)
        posts_paginator = Paginator(posts, POSTS_PER_PAGE)
        try:
            posts = posts_paginator.page(page)
        except PageNotAnInteger:
            posts = posts_paginator.page(POSTS_PER_PAGE)
        except EmptyPage:
            posts = posts_paginator.page(posts_paginator.num_pages)

        context['posts'] = posts

        
        return render(request, 'blog/home.html', context)

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    
    #comments = Comment.objects.filter(posts=posts).order_by('-id')

    #context = {
    #'posts' : posts,
    #'comment': comment,
    
     #}



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

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


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


