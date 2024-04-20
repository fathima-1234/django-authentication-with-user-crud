from django.db import models


class Profile(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    username= models.CharField(max_length=255)
    email=  models.CharField(max_length=255)

    def __str__(self):
        return self.username
