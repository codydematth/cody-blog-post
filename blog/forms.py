from django import forms
from .models import Comment, Reply, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "post_image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

        labels = {"body": ""}


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ("reply_body",)
        labels = {"reply_body": ""}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ReplyForm, self).__init__(*args, **kwargs)
