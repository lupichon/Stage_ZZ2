from django.db import models
from django.contrib.auth import get_user_model

class Data(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    measurement_date = models.DateTimeField(auto_now_add=True)
    gravity_center = models.JSONField()
    acceleration = models.JSONField()
    class Meta:
        ordering = ['-measurement_date']
