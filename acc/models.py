from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    refresh_token=models.CharField(max_length=200)
    access_token=models.TextField(max_length=200)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    posting_key=models.CharField(max_length=200, null=True)
    memo_key=models.CharField(max_length=200, null=True)
    active_key=models.CharField(max_length=200, null=True)

