from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from core.models import Post
from django.core.exceptions import ValidationError
# Create your models here.


class Comment(models.Model):
    content = models.TextField(null=False, blank=False)
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    username = models.TextField(max_length=255, blank=True, null=True)

    def clean(self):
        if self.user is None and self.username is None:
            raise ValidationError('Username is required')

    def __str__(self):
        return self.content[:20]

