
from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
# from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, null = True, blank = True)
    content = RichTextField(null =True, blank = True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

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

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # email = models.EmailField(max_length=100)
    content = RichTextField(max_length=10000, null= True, blank = True)
    date_posted = models. DateTimeField(default=timezone.now)
    # date_updated = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('date_posted',)

    def __str__(self):
        return self.user.username