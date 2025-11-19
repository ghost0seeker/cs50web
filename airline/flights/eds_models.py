from django.db import models

class Color(models.Model):
    color_code = models.CharField(max_length=2)
    color_name = models.CharField(max_length=10)

class Material(models.Model):
    material_code = models.CharField(max_length=4)
    material_description = models.TextField()

