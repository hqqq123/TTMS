from django.db import models

# Create your models here.
from authority.models import Auth


class Role(models.Model):
    name=models.CharField(max_length=20)
    auths=models.ManyToManyField(Auth)