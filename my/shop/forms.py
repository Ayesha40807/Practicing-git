from django import forms
from shop.models import CustomUser
from django.forms import ModelForm
from .models import *
from django.forms import forms
from django import forms




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['age','gender','photo']

class QuickPatientForm(ModelForm):
  detail =forms.CharField(widget=forms.Textarea)
  medicine_detail=forms.CharField(widget=forms.Textarea)
  amount =forms.IntegerField()
  next_visit =forms.IntegerField()
 
  class Meta:
    model=Patient
    fields=["name","age","gender","detail","medicine_detail","amount","next_visit"]

  def __init__(self,*args, **kwargs):
    super(QuickPatientForm,self).__init__(*args, **kwargs)
    for field in self.fields:
      self.fields[field].widget.attrs['class']='form-control'

class PatientForm(ModelForm):
  detail =forms.CharField(widget=forms.Textarea)
  medicine_detail=forms.CharField(widget=forms.Textarea)
  note=forms.CharField(widget=forms.Textarea)
  amount =forms.IntegerField()
  next_visit =forms.IntegerField()
  class Meta:
    model=Patient
    fields=["name","age","gender","email","detail","address","mobile","medicine_detail","amount","next_visit","note"]

  def __init__(self,*args, **kwargs):
    super(PatientForm,self).__init__(*args, **kwargs)
    self.fields['address'].required=False
    self.fields['address'].widget.attrs['rows']='5'
    self.fields['note'].widget.attrs['rows']='5'

    for field in self.fields:
      self.fields[field].widget.attrs['class']='form-control'

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ["patient", "detail", "medicine_detail", "amount", "next_visit", "note","old_medicines","morning","afternoon","evening","before_eating","after_eating"]
        widgets = {
            'old_medicines': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'morning': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'afternoon': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'evening': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'before_eating': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'after_eating': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # other widgets...
        }

    def __init__(self, *args, **kwargs):
        super(VisitForm, self).__init__(*args, **kwargs)
        self.fields['detail'].widget = forms.Textarea(attrs={'rows': 5, 'class': 'form-control'})
        self.fields['medicine_detail'].widget = forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'id': 'medicine-detail'})
        self.fields['note'].widget = forms.Textarea(attrs={'rows': 5, 'class': 'form-control'})
        self.fields['amount'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['next_visit'].widget = forms.NumberInput(attrs={'class': 'form-control'})

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'date', 'time']




class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'message',]