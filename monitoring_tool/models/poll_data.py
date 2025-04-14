from django.db import models
from .store import Store

class PollData(models.Model):
    ## model being used to store polling data 
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='poll_data')
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.store.store_id} - {self.timestamp_utc} - {self.status}"
