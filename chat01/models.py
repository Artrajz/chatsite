from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class users(AbstractUser):
    phone = models.BigIntegerField(null=True)

class group_list(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=32)


class group(models.Model):
    group_id = models.ForeignKey(group_list,on_delete=models.CASCADE,default="")
    user_id = models.IntegerField()


class contactors(models.Model):
    user_id = models.IntegerField()
    friend_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default="")


class message(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name = 'user_id_id',default="")
    talker_type = models.SmallIntegerField()
    talker_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name = 'talker_id_id',default="")
    create_time = models.DateTimeField()
    content = models.TextField()




