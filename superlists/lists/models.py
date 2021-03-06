from __future__ import unicode_literals
from django.db import models



class List(models.Model):
    name = models.TextField(default = '') #value empty string is reasonable bc its a text field,

class Item(models.Model): #models.Model leverages django to give us save method
    text = models.TextField(default = '') #value empty string is reasonable bc its a text field,
    list = models.ForeignKey(List, default = None)
    is_done = models.BooleanField(default = False)
