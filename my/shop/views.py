
from .models import *
from .forms import QuickPatientForm,PatientForm,VisitForm,ReminderForm,InquiryForm
from django.db import transaction,IntegrityError
import calendar
from django.db.models import Count,Sum
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect 
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserProfileForm
from django.core.mail import EmailMessage,send_mail
from django.urls import reverse_lazy
from datetime import date,datetime,timedelta
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
# Create your views here.
def home(request):
    return render(request,'home.html')

def add_patient(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        visit_form = VisitForm(request.POST)
        if visit_form.is_valid():
            try:
                with transaction.atomic():
                    patient_name = visit_form.cleaned_data['patient']
                    patient = Patient.objects.get(name=patient_name)
                    visit = Visit.objects.create(
                        patient=patient,
                        detail=visit_form.cleaned_data['detail'],
                        medicine_detail=visit_form.cleaned_data['medicine_detail'],
                        amount=visit_form.cleaned_data['amount'],
                        next_visit=visit_form.cleaned_data['next_visit'],
                        note=visit_form.cleaned_data['note'],
                        morning=visit_form.cleaned_data['morning'],
                        afternoon=visit_form.cleaned_data['afternoon'],
                        evening=visit_form.cleaned_data['evening'],
                        before_eating=visit_form.cleaned_data['before_eating'],
                        after_eating=visit_form.cleaned_data['after_eating']
                    )
                    visit.medicines.set(visit_form.cleaned_data['medicines'])
                    messages.success(request, 'Patient added successfully')
                    return redirect('add_patient')
            except IntegrityError:
                messages.warning(request, "Something went wrong!!")
        else:
            messages.warning(request, "Invalid form data")
    else:
        visit_form = VisitForm()
    return render(request, 'add-patient-form.html', {'visit_form': visit_form})


def quick_add_patient(request):
  if request.method=='POST':
      try:
        with transaction.atomic():
              form=QuickPatientForm(request.POST)
              if form.is_valid():
                  patient=form.save()
                  visit=Visit.objects.create(
                        patient=patient,
                        detail=form.cleaned_data['detail'],
                        medicine_detail=form.cleaned_data['medicine_detail'],
                        next_visit=form.cleaned_data['next_visit'],
                        amount=form.cleaned_data['amount'],
                  )
                 
                  messages.success(request,'Patient added successfully')
                  return redirect('quick_add_patient')
              else :
                  messages.warning(request,'Something went wrong')
                  return redirect('quick_add_patient')
      except IntegrityError:
          messages.warning(request,"Something went wrong!!")
          return redirect('quick_add_patient')
  else:
    form = QuickPatientForm
    return render(request,'quick-add-patient-form.html',{'form':form,'page_title':'Add Patient'})
 
def all_patients(request):
  data=Patient.objects.all().order_by('-id')
  return render(request,'all-patients.html',{'data':data})



def reports(request):
	selectedYear=date.today().year
	if request.GET.get('year'):
		selectedYear=request.GET.get('year')
      
	selectedMonth=date.today().month
	if request.GET.get('month'):
		selectedMonth=request.GET.get('month')
	#fetch Years
	years=Visit.objects.values('visit_date__year').annotate(total= Count('id'))
	print(years)

	#fetch months
	monthNames=[]
	months=Visit.objects.filter(visit_date__year = selectedYear).values('visit_date__month').annotate(total=Count('id'))
	for month in months:
		monthNames.append({'id':month['visit_date__month'],'name':calendar.month_name[month['visit_date__month']]})

	#charts by dates
	dPatients=Visit.objects.filter(visit_date__year=selectedYear,visit_date__month=selectedMonth).values('visit_date').annotate(total=Count('id'))
	dailyChartLabels=[]
	dailyChartValues=[]
	
	for data in dPatients:
		dailyChartLabels.append(data['visit_date'].strftime('%d-%m-%y'))
		dailyChartValues.append(data['total'])


	#charts by months
	mPatients=Visit.objects.filter(visit_date__year=selectedYear).values('visit_date__month').annotate(total=Count('id'))
	monthChartLabels=[]
	monthChartValues=[]

	for data in mPatients:
		monthName=calendar.month_name[data['visit_date__month']]
		monthChartLabels.append(monthName)
		monthChartValues.append(data['total'])

	#charts by Yearly
	yPatients=Visit.objects.values('visit_date__year').annotate(total=Count('id'))
	yearChartLabels=[]
	yearChartValues=[]

	for data in yPatients:
		yearName=data['visit_date__year']
		yearChartLabels.append(yearName)
		yearChartValues.append(data['total'])

	return render(request,'reports.html',{
      'dailyPatients':dPatients,
      'page_title':'Reports',
      'dailyChart':{
         'dailyChartLabels':dailyChartLabels,
         'dailyChartValues':dailyChartValues
         },
      'monthlyChart':{
         'monthlyChartLabels':monthChartLabels,
         'monthlyChartValues':monthChartValues
         },
      'yearlyChart':{
         'yearlyChartLabels':yearChartLabels,
         'yearlyChartValues':yearChartValues
         },
      'years':years,
      'currentYear':date.today().year,
      'currentMonth':int(selectedMonth),
      'monthNames':monthNames
})


def collection_reports(request):
	selectedYear=date.today().year
	if request.GET.get('year'):
		selectedYear=request.GET.get('year')
      
	selectedMonth=date.today().month
	if request.GET.get('month'):
		selectedMonth=request.GET.get('month')
	#fetch Years
	years=Visit.objects.values('visit_date__year').annotate(total= Count('id'))
	print(years)

	#fetch months
	monthNames=[]
	months=Visit.objects.filter(visit_date__year = selectedYear).values('visit_date__month').annotate(total=Count('id'))
	for month in months:
		monthNames.append({'id':month['visit_date__month'],'name':calendar.month_name[month['visit_date__month']]})

	#charts by dates
	dPatients=Visit.objects.filter(visit_date__year=selectedYear,visit_date__month=selectedMonth).values('visit_date').annotate(total=Sum('amount'))
	dailyChartLabels=[]
	dailyChartValues=[]
	
	for data in dPatients:
		dailyChartLabels.append(data['visit_date'].strftime('%d-%m-%y'))
		dailyChartValues.append(float(data['total']))


	#charts by months
	mPatients=Visit.objects.filter(visit_date__year=selectedYear).values('visit_date__month').annotate(total=Sum('amount'))
	monthChartLabels=[]
	monthChartValues=[]

	for data in mPatients:
		monthName=calendar.month_name[data['visit_date__month']]
		monthChartLabels.append(monthName)
		monthChartValues.append(float(data['total']))

	#charts by Yearly
	yPatients=Visit.objects.values('visit_date__year').annotate(total=Sum('amount'))
	yearChartLabels=[]
	yearChartValues=[]

	for data in yPatients:
		yearName=data['visit_date__year']
		yearChartLabels.append(yearName)
		yearChartValues.append(float(data['total']))

	return render(request,'collection_report.html',{
      'dailyPatients':dPatients,
      'page_title':'Reports',
      'dailyChart':{
         'dailyChartLabels':dailyChartLabels,
         'dailyChartValues':dailyChartValues
         },
      'monthlyChart':{
         'monthlyChartLabels':monthChartLabels,
         'monthlyChartValues':monthChartValues
         },
      'yearlyChart':{
         'yearlyChartLabels':yearChartLabels,
         'yearlyChartValues':yearChartValues
         },
      'years':years,
      'currentYear':date.today().year,
      'currentMonth':int(selectedMonth),
      'monthNames':monthNames
})


@login_required
def index_doctor(request):
    patient_name = request.user.username  # Assuming the username is used as the patient name
    return render(request, 'index_doctor.html', {'patient_name': patient_name})

@login_required
def index(request):
    patient_name = request.user.username  # Assuming the username is used as the patient name
    return render(request, 'index.html', {'patient_name': patient_name})

def successful_profile(request):
    return render(request,'successful_profile.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            user_type = user.user_type
            
            if user_type == 'patient':
                return redirect('index')  # Redirect to patient info page
            elif user_type == 'doctor':
                return redirect('index_doctor')  # Redirect to master page for doctors
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        user_type = request.POST['user_type']
        
        if password1 == password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    user_type=user_type
                )
                user.save()
                print('User created')
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')
  
def logout(request):
  auth.logout(request)
  return redirect('/')

def options(request):
   return render(request, 'options.html')

def info(request):
   return render(request,'info.html')


def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form,'patient': user})


def update_patient(request,id):
  patient=Patient.objects.get(id=id)
  if request.method=='POST':
    form = PatientForm(request.POST,instance=patient)
    if form.is_valid():
      form.save()
      messages.success(request,'Patient updated successfully')
      return redirect('update_patient',id)
    else:
      messages.warning(request,'Something went wrong')
      return redirect('update_patient',id)

  else:
    form = PatientForm(instance=patient)
    return render(request,'update-patient-form.html',{'form':form})


def delete_patient(request,id):
  Patient.objects.get(id=id).delete()
  messages.success(request,"Patient deleted successfully")
  return redirect('all_patients')

def email_template(request):
  return render(request,'email_template.html')

def n_patients(request):
    today = date.today()
    patients = Visit.objects.filter(visit_date__lt=today)

    count = 0
    for patient in patients:
        nextVisitDate = patient.visit_date + timedelta(days=patient.next_visit)
        notificationDate = nextVisitDate - timedelta(days=1)
        
        if notificationDate == today:
            subject=f'Doctor next visit'
            msg=render_to_string('email_template.html',{'next_visit':nextVisitDate,'patient':patient})
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[patient.patient_email(),]
            mail=EmailMessage(subject,msg,email_from,recipient_list)
            mail.content_subtype  ="html"
            mail.send()
            count+=1  
    return render(request, 'n_patients.html', {
        'patients': patients,
        'count': count
    })

@login_required
def patient_dashboard(request):
    patient = Patient.objects.order_by("patient_name")
    return render(request, 'dashboard.html', {'patient': patient})



from django.db import IntegrityError
def add_visit(request,patient_id):
  if request.method=='POST':
    patient=Patient.objects.get(id=patient_id)
    form = VisitForm(request.POST)
    if form.is_valid():
            
            form.patient=patient
            visit=form.save(commit=False)
            visit.patient=patient
            form.save()
            messages.success(request,'Visit added successfully')
            return redirect(reverse_lazy('add_visit',kwargs={'patient_id':patient_id}))
    else :
            print(form.errors)
            messages.warning(request,'Something went wrong!!')
            return redirect(reverse_lazy('add_visit',kwargs={'patient_id':patient_id}))
  else:
    form = VisitForm
    return render(request,'visit-form.html',{'form':form,
                                             'page_title':'Add Visit'})




def patient_detail(request):
    return render(request,'patient_detail.html')

def Quick_Statistics(request):
  totalPatients=Patient.objects.count()
  totalCollection=Visit.objects.aggregate(total=Sum('amount'))
  return render(request,'Quick_Statistics.html',{'page_title':'Dashboard','totalPatients':totalPatients,'totalCollection':totalCollection})

def schedule(request): 
    medicines = Reminder.objects.all() 
    if request.method=="POST":
        form =ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        form =ReminderForm()
    return render(request, 'schedule.html', {'form': form, 'medicines': medicines})

def create_reminder(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)  # Use the ReminderForm for validation
        if form.is_valid():
            form.save()  # Save the form data
            return redirect('index')
    else:
        form = ReminderForm()  # Create a new form for GET requests
    return render(request, 'create_reminder.html', {'form': form})

def pricing(request):
    return render(request,'pricing.html')
def faq(request):
    return render(request,'faq.html')



def inquiry_page(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inquiry_success')
    else:
        form = InquiryForm()
    return render(request, 'inquiry_page.html', {'form': form})

def inquiry_success(request):
    return render(request, 'inquiry_success.html')


def inquiry_list(request):
    inquiries = Inquiry.objects.all()
    return render(request, 'inquiry_list.html', {'inquiries':inquiries})

def add_room(request):
    return render(request, 'add-room.html')
def edit_room(request):
    return render(request, 'edit-room.html')

def add_payment(request):
    return render(request, 'add-payment.html')

def about_payment(request):
    return render(request, 'about-payment.html')

def patient_profile(request,id):
    # Assuming the patient is authenticated and their ID is stored in the session
    patient = Patient.objects.get(pk=id)

    # Retrieve all visits associated with the patient
    patient_visits = PatientVisit.objects.filter(patient=patient)

    # Pass the patient and visit information to the template
    return render(request, 'patient_profile.html', {'patient': patient, 'patient_visits': patient_visits})

def medication_details(request):
    if request.user.is_authenticated and request.user.user_type == 'patient':
        patient = request.user
        visits = Visit.objects.filter(patient=patient)
        visit_details = []

        for visit in visits:
            # Get all medicines related to the current visit through the PatientVisitMedicine model
            patient_visit_medicines = Medicine.objects.filter(patient=patient, visit=visit)
            medicine_names = [pvm.medicine.medicine_name for pvm in patient_visit_medicines]
            
            medicine_detail = {
                'visit_date': visit.visit_date,
                'medicine_names': medicine_names,
                'morning': visit.morning,
                'afternoon': visit.afternoon,
                'evening': visit.evening,
                'before_eating': visit.before_eating,
                'after_eating': visit.after_eating,
            }
            visit_details.append(medicine_detail)

        # Debugging: Print visit details to console
        print("Visit Details:", visit_details)

        return render(request, 'medication_details.html', {'medicine_details': visit_details})
    else:
        return render(request, 'login.html', {'error': 'User is not authenticated or not a patient'})
    
    # views.py
from rest_framework import viewsets
from .models import Patient, Visit, Medicine
from .serializers import PatientSerializer, VisitSerializer, MedicineSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

