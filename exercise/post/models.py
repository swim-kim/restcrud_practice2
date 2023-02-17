from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, blank=False)
    bio = models.TextField(max_length=500, blank=True)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField

class Post (models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE)
    content = models.TextField(max_length = 200)
    created_at = models.DateField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, related_name='tag',blank=True)
    like_user_set = models.ManyToManyField(Profile,blank = True, related_name = 'likes_user_set', through = 'Like')

    @property
    def like_count(self):
        return self.like_user_set.count()
