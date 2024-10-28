from django.db import models
from django.utils.text import slugify
# Create your models here.


def avatar_upload_path(instance, filename):

    username = slugify(instance.username)
    return f'avatars/{username}'


class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    img_path = models.ImageField(upload_to=avatar_upload_path)

    class Meta:
        db_table = 'img_path'
