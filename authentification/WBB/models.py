from django.db import models
from django.contrib.auth import get_user_model

class Data(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    session_id = models.IntegerField(default=1)
    shot_id = models.IntegerField(default=1)
    measurement_date = models.DateTimeField(auto_now_add=True)
    gravity_center = models.JSONField()
    #acceleration = models.JSONField()
    quaternion = models.JSONField()
    height = models.FloatField()
    width = models.FloatField()
    class Meta:
        ordering = ['-measurement_date']
