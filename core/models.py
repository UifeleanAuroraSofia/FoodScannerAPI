from django.db import models

class DangerousSubstance(models.Model):
    name_ro = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    abbreviation = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.name_ro} ({self.abbreviation}) - {self.description}"
