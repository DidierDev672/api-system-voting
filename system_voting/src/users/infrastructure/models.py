from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class UserModel(AbstractBaseUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20)