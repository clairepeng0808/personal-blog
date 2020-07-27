from django.db import models
from django.utils import timezone
from django.urls import reverse,reverse_lazy
from django.contrib import messages



# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)
    # publish_date can be null

    def get_comments(self):
        return Comment.objects.filter(post__pk=self.pk).order_by('-create_date')

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def approved_comment(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=128)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve_comment(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('list', kwargs={'pk': self.pk})

    def __str__(self):
        return self.text
