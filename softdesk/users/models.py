from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from datetime import date, timedelta


class UserManager(BaseUserManager):
    """Define a model manager for the User model"""

    use_in_migrations = True

    def create_user(self, email, username, dob, password, **extra_fields):
        """Create and save a User with the given email, username, dob, and password."""
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username, 
            dob=dob, 
            can_be_contacted=extra_fields.pop('can_be_contacted', False),
            can_data_be_shared=extra_fields.pop('can_data_be_shared', False),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """User model without first_name & last_name."""

    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    dob = models.DateField(help_text="Date de naissance de l'utilisateur (YYYY-MM-DD)")
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

    # Remove fields no longer needed
    first_name = None
    last_name = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "dob"]

    objects = UserManager()

    def calculate_age(self):
        """Calcule l'âge de l'utilisateur à partir de la date de naissance."""
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age

    class Meta:
        ordering = ["email"]

    @property
    def user_id(self):
        """Return pk attribute of the object."""
        return self.pk

    def __str__(self):
        """String representation of the User."""
        return f"{self.user_id}, {self.username}, {self.email}"
