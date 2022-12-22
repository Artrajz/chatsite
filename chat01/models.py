from django.db import models


class group_list(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=32)


class group(models.Model):
    group_id = models.ForeignKey(group_list,on_delete=models.CASCADE,default="")
    user_id = models.IntegerField()


class contactors(models.Model):
    user_id = models.IntegerField()
    friend_id = models.IntegerField()


class message(models.Model):
    user_id = models.IntegerField()
    talker_type = models.SmallIntegerField()
    talker_id = models.IntegerField()
    create_time = models.DateTimeField()
    content = models.TextField()


