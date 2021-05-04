from django.db import models
from django.conf import settings


class Medication(models.Model):
    patient_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,)
    date = models.DateField()
    doctor_name = models.CharField(max_length=100)
    reason = models.CharField(max_length=200)
    drugs = models.CharField(max_length=200)

    def __str__(self):
        return "%s - %s" %(self.patient_ID, self.drugs)
