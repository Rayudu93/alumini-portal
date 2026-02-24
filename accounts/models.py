# api/models.py
import random
from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

def generate_custom_id():
    year = str(datetime.now().year)[-2:]        # last 2 digits of year
    random_digits = str(random.randint(10000, 99999))  # 5 random digits
    return f"1{year}{random_digits}"

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    ALUMNI = "ALUMNI"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (STUDENT, "Student"),
        (ALUMNI, "Alumni"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES,null=True,)
    custom_id = models.CharField(max_length=8, unique=True, editable=False, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Assign custom_id only if it doesn't exist
        if not self.custom_id:
            self.custom_id = generate_custom_id()
        super().save(*args, **kwargs)

    def __str__(self):
        # Display the custom ID instead of default id
        return self.custom_id or str(self.id)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    department = models.CharField(max_length=100)
    graduation_year = models.PositiveIntegerField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.email


class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="alumni_profile")
    company = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
