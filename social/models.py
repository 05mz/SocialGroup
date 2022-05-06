
# Create your models here.
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, GroupManager, Group
# from permissions.utils import register_role, grant_permission


class User(AbstractUser):
    role = models.CharField(max_length=10, null=True)
    id = models.AutoField(primary_key=True)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        ("username"),
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )


class Comment(models.Model):
    # post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    id = models.AutoField(primary_key=True)
    body = models.TextField(("comments"))
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return '{} by {}'.format(self.body, self.name)


class Post(models.Model):
    ACCESS_PUBLIC = 0
    ACCESS_PRIVATE = 1
    ACCESS_LEVEL_CHOICES = [
        (ACCESS_PUBLIC, 'Public'),
        (ACCESS_PRIVATE, 'Private'),
    ]

    contents = models.CharField(max_length=140)
    # comments = models.ForeignKey(Comment, on_delete=models.CASCADE,)
    comments = models.ManyToManyField(
        Comment,
        blank=True,
    )
    # comments = models.CharField(max_length=200)
    access_level = models.IntegerField(choices=ACCESS_LEVEL_CHOICES, default=ACCESS_PRIVATE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class SocialGroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class SocialGroup(models.Model):
    name = models.CharField(("group_name"), max_length=150, unique=True)
    group_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("group_permissions"),
        blank=True,
    )
    user_list = models.ManyToManyField(
        User,
        related_name='users',
        # verbose_name=("user_list"),
        blank=True,
    )
    posts = models.ManyToManyField(
        Post,
        verbose_name=("posts"),
        blank=True,
    )
    admin_username = models.ForeignKey(User, related_name='admin', on_delete=models.CASCADE) #unable to figure out how to give only one user special permissions
    objects = SocialGroupManager()
    # owner = register_role("Owner")
    # grant_permission(Post, owner, "edit")

    class Meta:
        verbose_name = ("social_group")
        verbose_name_plural = ("social_groups")

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

