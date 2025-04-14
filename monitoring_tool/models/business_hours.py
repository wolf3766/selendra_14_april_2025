from django.db import models
from .store import Store

class BusinessHours(models.Model):
    ## model used to store business hours data 
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='business_hours')
    dayOfWeek = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f"{self.store.store_id} - Day {self.dayOfWeek}"
