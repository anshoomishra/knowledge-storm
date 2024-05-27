from django.db import models
from account.models import User
# Create your models here.


class Test(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="owner")
    updated_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="updator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_marks = models.IntegerField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=200)
    test = models.ForeignKey(Test,null=True, blank=True, on_delete=models.SET_NULL)  # ToDo check if
    pass

class Answer(models.Model):
    pass

