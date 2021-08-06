from recognizer import recognizer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages


from useraccount.models import Medication
from account.models import Account

from .forms import MedicationForm


def temphomeview(request):
    return redirect('home')


@login_required
def homeview(request):
    return render(request, 'useraccount/homepage.html')


@login_required
def userprofileview(request):
    user = request.user
    meds = user.medication_set.all()
    context = {'patient': user, 'medications': meds}
    return render(request, 'useraccount/patientinfo.html', context)

# all users view


@login_required
@permission_required('is_superuser')
def allusersview(request):
    users = Account.objects.exclude(is_superuser=True)
    context = {'accounts': users}
    return render(request, 'useraccount/users/allusers.html', context)

# find patient view


@login_required
@permission_required('is_doctor')
def findpatientview(request):
    context = {}
    if request.method == "GET":
        if request.GET.get('search') == "Search":
            sval = request.GET.get("searchbox")
            if sval == "" or sval == " ":
                messages.error(request, "Enter Patient ID or Name")
                return redirect("findpatient")
            p_list = Account.objects.filter(
                userID__icontains=sval) | Account.objects.filter(username__icontains=sval)
            p_list = p_list.exclude(is_doctor=True)
            if not p_list:
                messages.error(request, "Patient not Found!")
            else:
                context = {"p_list": p_list}
        if request.GET.get('search') == "Search by Face":
            names = recognizer()
            p_list = []
            for name in names:
                temp = Account.objects.filter(username=name)
                if not temp:
                    p_list.append(temp)
            if not p_list:
                messages.error(request, "Patient not Found!")
            else:
                context = {"p_list": p_list}

    return render(request, 'useraccount/doctor/findpatient.html', context)


# all patient view

@login_required
@permission_required('is_doctor')
def allpatientsview(request):
    patients = Account.objects.exclude(is_doctor=True)
    context = {'patients': patients}
    return render(request, 'useraccount/doctor/allpatients.html', context)


# medications views


@login_required
def patientprofileview(request, id):
    pat = Account.objects.filter(userID=id)
    if not pat:
        return HttpResponse("<h1 align=center>No Patient Found!!!<h1>")
    patient = pat.first()
    meds = patient.medication_set.all()
    context = {'patient': patient, 'medications': meds}

    return render(request, 'useraccount/patientinfo.html', context)


@login_required
def addmedview(request, id):
    patient = Account.objects.get(userID=id)
    newmed = MedicationForm(request.POST or None)
    if request.method == 'POST':
        if newmed.is_valid():
            temp = newmed.save(commit=False)
            temp.patient_ID = patient
            temp.save()
            return redirect('patientprofile', id=patient)
    context = {'patient': patient, 'medform': newmed,
               'button': 'Add', 'head': 'Add'}

    return render(request, 'useraccount/medication/updatemed.html', context)


@login_required
def deltemedview(request, pk):
    meditem = Medication.objects.get(pk=pk)
    patient = Account.objects.get(userID=meditem.patient_ID)

    if request.method == 'POST':
        meditem.delete()
        return redirect('patientprofile', id=patient)
    context = {'patient': patient, 'meditem': meditem}

    return render(request, 'useraccount/medication/deletemed.html', context)


@login_required
def editmedview(request, pk):
    meditem = Medication.objects.get(pk=pk)
    patient = Account.objects.get(userID=meditem.patient_ID)
    editform = MedicationForm(instance=meditem)

    if request.method == 'POST':
        editform = MedicationForm(request.POST, instance=meditem)
        if editform.is_valid():
            editform.save()
            return redirect('patientprofile', id=patient)
    context = {'patient': patient, 'medform': editform,
               'button': 'Save', 'head': 'Edit'}

    return render(request, 'useraccount/medication/updatemed.html', context)
