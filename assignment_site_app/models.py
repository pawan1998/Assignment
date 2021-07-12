# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserSearchDetails(models.Model):
    user = models.ForeignKey(User) 
    keyword = models.CharField(max_length=100) # ToDO : Red alert over 100
    result = models.TextField() #String stringToBeInserted = jsonObject.toString(); JSONObject jsonObject = new JSONObject(json);
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
         return str(self.user)



    
