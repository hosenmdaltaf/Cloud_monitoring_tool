# models.py

from django.db import models

class MetricData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_utilization = models.FloatField(null=True, blank=True)
    memory_utilization = models.FloatField(null=True, blank=True)
    disk_utilization = models.FloatField(null=True, blank=True)
    network_in = models.FloatField(null=True, blank=True)
    network_out = models.FloatField(null=True, blank=True)
    cpu_credit_balance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Metrics at {self.timestamp}"
