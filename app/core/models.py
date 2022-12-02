"""
Database models.
"""
import os
import uuid

from django.core.validators import MaxLengthValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads', 'article', filename)


class UserManager(BaseUserManager):
    """Managers for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """Return string representation of our user."""
        return f"{self.first_name} {self.last_name}"


class Article(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    preview = models.CharField(max_length=255)
    body = models.TextField()
    cover = models.ImageField(null=True, upload_to=image_file_path)
    categories = models.ManyToManyField('Category')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(validators=[MaxLengthValidator(1500)])
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

