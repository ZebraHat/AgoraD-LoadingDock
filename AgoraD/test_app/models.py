__author__ = 'chase'


from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)

    class Meta:
        app_label = 'test_app'


class Place(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    zip_code = models.IntegerField(max_length=5)

    class Meta:
        app_label = 'test_app'