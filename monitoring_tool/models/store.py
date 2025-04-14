from django.db import models

class Store(models.Model):
    ## model being used to store stores with timezone. 
    store_id = models.CharField(primary_key=True, max_length=255)
    timezone_str = models.CharField(max_length=100, default='America/Chicago')

    def __str__(self):
        return self.store_id
