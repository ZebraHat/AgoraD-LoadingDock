#
## models.py
## Meaningless models to test the loading dock
#

__author__ = 'chase'


from django.db import models


class Student(models.Model):
    def __unicode__(self):
        return str(self.name)

    name = models.CharField(max_length=50)
    sid = models.CharField(max_length=50)

    class Meta:
        app_label = 'test_app'


class Food_Type(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        app_label = 'test_app'


class Food(models.Model):
    def __unicode__(self):
        return str(self.name)

    eaten_by = models.ForeignKey(Student)
    type = models.ForeignKey(Food_Type)
    price = models.FloatField()

    class Meta:
        app_label = 'test_app'