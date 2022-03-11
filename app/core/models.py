from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings

STATUS_CHOICES = [
    ("Installation Requested", "Installation Requested"),
    ("Installation in Progress", "Installation in Progress"),
    ("Installation Complete", "Installation Complete"),
    ("Installation Rejected", "Installation Rejected"),
]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    # Customise username email form username to email
    USERNAME_FIELD = "email"


class Installation(models.Model):
    """Installation object"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    appointment_date = models.DateField(auto_created=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.customer_name

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Installation, self).save(*args, **kwargs)
            Status.objects.create(
                status=STATUS_CHOICES[0][0], notes="Created", installation=self
            )
        else:
            super(Installation, self).save(*args, **kwargs)


class Status(models.Model):
    """Status to be used to track progress of installs"""

    status = models.CharField(
        max_length=255, default=STATUS_CHOICES[0][0], choices=STATUS_CHOICES
    )
    notes = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now=True)
    installation = models.ForeignKey(
        Installation,
        related_name="status",
        on_delete=models.CASCADE,
        default=None,
        null=True,
    )

    def __str__(self) -> str:
        return self.status
