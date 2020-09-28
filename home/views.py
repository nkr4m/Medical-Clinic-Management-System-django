from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.db.models import Sum

# Create your views here.
from .forms import AppoinmentForm, CreateUserForm, PatientForm
from django.forms import inlineformset_factory

# filter package
from .filters import AppoinmentFilter

# permissions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# auth
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')



			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
			

	context = {'form':form}
	return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')




# ----------------------------------------admins-only-------------------------------------------------
@login_required(login_url='login')
@admin_only
def dashboard(request):

    patients = Patient.objects.all()
    appoinments = Appoinment.objects.all()

    total_appoinments = appoinments.count()
    examinations = appoinments.filter(status='Examination').count()
    discharged = appoinments.filter(status='Discharged').count()

    context = {'appoinments': appoinments, 'patients': patients,
               'total_appoinments': total_appoinments, 'examinations': examinations, 'discharged': discharged}

    return render(request, 'dashboard.html', context)

    return render(request, 'dashboard.html')


#--------------------USER PAGE -----------------------#

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def userPage(request):

    #get all appoinments of the particular patient
    appoinments = request.user.patient.appoinment_set.all()
    

    context = {'appoinments':appoinments}
    return render(request, 'userPage.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def account_settings(request):
	patient = request.user.patient
	form = PatientForm(instance=patient)

	if request.method == 'POST':
		form = PatientForm(request.POST, request.FILES,instance=patient)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'account_settings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def medications(request):
    treatment = Treatment.objects.all()
    context = {'treatment': treatment}
    return render(request, 'medications.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def patient(request, pk_test):

    patient = Patient.objects.get(id=pk_test)

    appointments = patient.appoinment_set.all()
    appointment_count = appointments.count()

    myFilter = AppoinmentFilter(request.GET, queryset=appointments)
    appointments = myFilter.qs

    context = {'patient': patient, 'appointment_count': appointment_count,
               'appointments': appointments, 'myFilter':myFilter}
    return render(request, 'patients.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def statistics(request):

    #-----------------patient count-------------------------
    patients = Patient.objects.all()
    appoinments = Appoinment.objects.all()
    treatments = Treatment.objects.all()
    total_treatments = treatments.count()

    #-------------------total Superusers--------------------
    superusers = User.objects.filter(is_superuser=True)
    superuser_count = int(superusers.count())


    #-------------------total users--------------------
    users = User.objects.all()
    users_all = int(users.count())
    users_count =  users_all - superuser_count

    total_appoinments = appoinments.count()
    examinations = appoinments.filter(status='Examination').count()
    discharged = appoinments.filter(status='Discharged').count()

    context = {'appoinments': appoinments, 'patients': patients,
               'total_appoinments': total_appoinments, 'examinations': examinations, 'discharged': discharged, 'total_treatments':total_treatments, 'superuser_count':superuser_count, 'users_count':users_count}

    return render(request, 'statistics.html', context)

# -----------------------crud-------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createAppoinment(request, pk):
    AppoinmentFormSet = inlineformset_factory(
        Patient, Appoinment, fields=('treatment', 'status'), extra=2)
    patient = Patient.objects.get(id=pk)
    # form = AppoinmentForm(initial={'patient': patient})
    formset = AppoinmentFormSet(
        queryset=Appoinment.objects.none(), instance=patient)
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # form = AppoinmentForm(request.POST)
        formset = AppoinmentFormSet(request.POST, instance=patient)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateAppoinment(request, pk):

    order = Appoinment.objects.get(id=pk)
    form = AppoinmentForm(instance=order)

    if request.method == 'POST':
        form = AppoinmentForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteAppoinment(request, pk):
    order = Appoinment.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'delete.html', context)


# -----------------------crud-------------------------------------------------
