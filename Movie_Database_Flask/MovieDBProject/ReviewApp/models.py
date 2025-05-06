from django.db import models
from django.contrib.auth.models import User
from MovieDBApp.models import Movie
from django.utils.timezone import now
# Create your models here.

class UserReview(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    parentReview=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13]+".... " 