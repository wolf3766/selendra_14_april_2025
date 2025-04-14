from django.db import models

class JobStore(models.Model):
    ##Table used to store jobs status which are being created
    
    STATUS_CHOICES = [
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed")
    ]

    job_id = models.CharField(primary_key=True, max_length=255)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.job_id} - {self.status}"