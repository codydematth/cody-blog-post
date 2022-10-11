from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

# from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    post_image = models.ImageField(upload_to="post_images")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    # def save(self, *args, **kwargs):
    #     if self.slug == None:
    #         slug = slugify(self.title)

    #         has_slug = Post.objects.filter(slug=slug).exists()
    #         count = 1
    #         while has_slug:
    #             count+= 1
    #             slug = slugify(self.title) + '-' + str(count)
    #             has_slug = Post.objects.filter(slug=slug).exists()

    #         self.slug = slug

    #     super().save(*args, **kwargs)


class Comment(models.Model):
    post_name = models.ForeignKey(
        Post, null=True, on_delete=models.CASCADE, related_name="comments"
    )
    comm_name = models.CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(max_length=500, blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.comm_name = slugify(
            "comment by" + "-" + str(self.author) + str(self.date_added)
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ["-date_added"]


class Reply(models.Model):
    comment_name = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    reply_body = RichTextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)
