import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user_ratings = models.IntegerField()

    class Meta:
        pass

    def __str__(self):
        return self.first_name + " " + self.last_name

    def full_name(self):
        return self.first_name + " " + self.last_name
