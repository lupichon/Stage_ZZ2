from django.db import models
from django.contrib.auth import get_user_model

class GravityMeasurement(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    measurement_date = models.DateTimeField(auto_now_add=True)
    center_of_gravity_x = models.FloatField()
    center_of_gravity_y = models.FloatField()
    class Meta:
        ordering = ['-measurement_date']
