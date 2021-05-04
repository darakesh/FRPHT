from django.contrib import admin

from useraccount.models import Medication
# Register your models here.

# @admin.register(UserAccount)
# class UserAccountAdmin(admin.ModelAdmin):
#     list_display = ('userid','age','gender','blood_group')
#     search_fields = ('userid',)

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('patient_ID','doctor_name','drugs')
    search_fields = ('drugs','doctor_name','patient_ID')
