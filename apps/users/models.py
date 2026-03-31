from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    points = models.IntegerField(default=0)
    total_pages_read = models.IntegerField(default=0)
    date_of_birth = models.DateField(blank=True, null=True)
    following_users = models.ManyToManyField(
        'self',
        through='social.Follow',
        through_fields=('follower', 'following'),
        symmetrical=False,
        related_name='follower_users'
    )

    def __str__(self):
        return self.username
