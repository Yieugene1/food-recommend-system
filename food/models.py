from django.db import models


# Create your models here.
class Userinfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)


class Userinfo1(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    hobby1 = models.CharField(max_length=64, default="")
    hobby2 = models.CharField(max_length=64, default="")
    hobby3 = models.CharField(max_length=64, default="")


class mypicture(models.Model):
    user = models.CharField(max_length=64)
    intro = models.CharField(max_length=300, default="")
    score = models.CharField(max_length=32, default="")
    class1 = models.CharField(max_length=32, default="")
    class2 = models.CharField(max_length=32, default="")
    taste = models.CharField(max_length=32, default="")
    country = models.CharField(max_length=32, default="")
    method1 = models.CharField(max_length=300, default="")
    save_num = models.IntegerField(default="")
    main_id = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='photos', default='user1.jpg')


class motivation(models.Model):
    user_name = models.CharField(max_length=64, default="")
    food_id = models.CharField(max_length=64, default="")
    food_name = models.CharField(max_length=300, default="")
    food_comment = models.CharField(max_length=300, default="")
    user_score = models.FloatField()


class user_save(models.Model):
    user_name = models.CharField(max_length=64, default="")
    food_photo = models.CharField(max_length=64, default="")
    food_name = models.CharField(max_length=300, default="")
    score = models.CharField(max_length=64, default="")


class browse(models.Model):
    user_name = models.CharField(max_length=64, default="")
    main_id = models.IntegerField(default=1)


class qitaguo(models.Model):
    country = models.CharField(max_length=64, default="")
