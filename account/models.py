from django.db import models

# Create your models here.
from role.models import Role


class Account(models.Model):
    # account=models.CharField(max_length=20,db_index=True)
    email=models.EmailField()
    password=models.CharField(max_length=200)
    name=models.CharField(max_length=20)
    # root=models.BooleanField()
    role=models.ForeignKey(Role,on_delete=models.SET_NULL,null=True)

