from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for the User model"""

    use_in_migrations = True

    def create_user(self, email, username, age, password, **extra_fields):
        """Create and save a User with the given email, username, age, and password."""
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username, 
            age=age, 
            can_be_contacted=extra_fields.pop('can_be_contacted', False),
            can_data_be_shared=extra_fields.pop('can_data_be_shared', False),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, age, password=None, **extra_fields):
        """Create and save User with the given email, username, and age."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, age, password, **extra_fields)

    def create_superuser(self, email, username, age, password, **extra_fields):
        """Create and save a SuperUser with the given email, username, and age."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, age, password, **extra_fields)


class User(AbstractUser):
    """User model without first_name & last_name."""

    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

    # Remove fields no longer needed
    first_name = None
    last_name = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "age"]

    objects = UserManager()

    class Meta:
        ordering = ["email"]

    @property
    def user_id(self):
        """Return pk attribute of the object."""
        return self.pk

    def __str__(self):
        """String representation of the User."""
        return f"{self.user_id}, {self.username}, {self.email}"
