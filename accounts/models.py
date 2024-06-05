from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    npm = models.CharField(
        max_length=8, 
        unique=True, 
        validators=[RegexValidator(r'^\d{8}$', 'NPM must be exactly 8 digits')],
        help_text="Nomor Pokok Mahasiswa consisting of exactly 8 digits.",
        null=True,
        blank=False
    )
    email = models.EmailField(unique=True, blank=False)