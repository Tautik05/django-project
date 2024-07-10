from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):

    peoples =[
        {'name' : 'Abhijeet Gupta' , 'age' :26},
        {'name' : 'Rohan Sharma' , 'age' :23},
        {'name' : 'Deepanshu Chaurasiya' , 'age' :2},
        {'name' : 'Sandeep' , 'age' :6},

    ]

    vegetables = ['Pumpkin', 'Tomato', 'Potato']



    return render(request,"index.html",context = {'peoples' : peoples ,'vegetables' : vegetables})



def about(request) :
      return render(request,"about.html")
def contact(request):
      return render(request,"contact.html")
def success_page(request):
    return HttpResponse("<h1>Hey this a Success page</h1>")