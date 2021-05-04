from django import forms
from useraccount.models import Medication

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = '__all__'
        exclude = ['patient_ID',]
