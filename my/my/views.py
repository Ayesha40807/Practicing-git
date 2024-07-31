from django.shortcuts import render,redirect
from django.db import models
from django.conf import settings

def happy(request):
    product=[{'name':'Product1','price':23},
             {'name':'Product2','price':32},
             {'name':'Product3','price':44}]
    context={'product':product}
    return render(request,'happy.html',context)