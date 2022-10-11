from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from operator import attrgetter
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from .models import Post, Comment
from .forms import CommentForm, ReplyForm, PostForm

POSTS_PER_PAGE = 5


def home(request):
    posts = Post.objects.all()
    posts = sorted(Post.objects.all(), key=attrgetter("date_posted"), reverse=True)
    # Search
    query = request.GET.get("q")
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(author__username=query)
        ).distinct()

    context = {
        "posts": posts,
    }

    # Pagination
    page = request.GET.get("page", 1)
    posts_paginator = Paginator(posts, POSTS_PER_PAGE)
    try:
        posts = posts_paginator.page(page)
    except PageNotAnInteger:
        posts = posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        posts = posts_paginator.page(posts_paginator.num_pages)

    context["posts"] = posts

    return render(request, "blog/home.html", context)


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView, FormView):
    model = Post

    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.form_class(request=self.request)
        if "form2" not in context:
            context["form2"] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "form" in request.POST:
            form_class = self.get_form_class()
            form_name = "form"
        else:
            form_class = self.second_form_class
            form_name = "form2"

        form = self.get_form(form_class)
        # print("the form name is : ", form)
        # print("form name: ", form_name)
        # print("form_class:",form_class)

        if form_name == "form" and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name == "form2" and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy("post-detail", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.post_name = self.object.comments.name
        fm.post_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get("comment.id")
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    # comments = Comment.objects.filter(posts=posts).order_by('-id')

    # context = {
    #'posts' : posts,
    #'comment': comment,

    # }


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        post_image = form.cleaned_data["post_image"]
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        post_image = form.cleaned_data["post_image"]
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
