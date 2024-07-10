from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from vege.seed import *
from django.core.paginator import Paginator
from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()

#from django.http import HttpResponse

# Create your views here.


@login_required(login_url="/login/")
def recipes(request):

   if request.method == "POST":
     data=request.POST

     recipe_image = request.FILES.get('recipe_image')
     recipe_name = data.get('recipe_name')
     recipe_description = data.get('recipe_description')
    
     print(recipe_description)
     print(recipe_name)
     print(recipe_image)

     Recipe.objects.create(
        recipe_name= recipe_name,
        recipe_image= recipe_image,
        recipe_description= recipe_description,
     )

     return redirect('recipes') 
    

   queryset = Recipe.objects.all()

   if request.GET.get('search'):
      #print(request.GET.get('search'))
      queryset = queryset.filter(recipe_name__icontains = request.GET.get('search'))

   context = {'recipes': queryset} 
   return render(request , 'recipes.html',context)


# def update_recipe(request, id):
#    queryset = Recipe.objects.get(id=id)

#    if request.method == "POST":
#      data = request.POST

#      recipe_image = request.FILES.get('recipe_image')
#      recipe_name = data.get('recipe_name')
#      recipe_description = data.get('recipe_description')

#      queryset.recipe_name=recipe_name
#      queryset.recipe_description=recipe_description

#      if recipe_image:
#         queryset.recipe_image = recipe_image

#    queryset.save()  
#    return redirect('recipes')

#    context = {'recipes': queryset} 
#    return render(request,'updaterecipes.html',context)

@login_required(login_url="/login/")
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST

        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        return redirect('recipes')

    context = {'recipes': queryset}  # Use 'recipe' instead of 'recipes'
    return render(request, 'update_recipes.html', context)
   


@login_required(login_url="/login/")
def delete_recipe(request, id):
   queryset = Recipe.objects.get(id = id)
   queryset.delete()
   return redirect('recipes')


def login_page(request):
   if request.method == "POST":
      username = request.POST.get('username')
      password = request.POST.get('password')

      if not User.objects.filter(username = username).exists():
         messages.info(request, 'Invalid user name')
         return redirect('/login')
      
      user = authenticate(username = username, password=password)

      if user is None:
        messages.error(request, 'Invalid password')
        return redirect('/login')
      
      else:
         login(request, user)
         return redirect('/recipes')
   

   return render(request, 'login.html')


def logout_page(request):
   logout(request)
   return redirect('/login')

def register(request):

   if request.method == "POST":
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      username = request.POST.get('username')
      password = request.POST.get('password')


      user=User.objects.filter(username = username)
      
      if user.exists():
         messages.info(request, 'Username already taken')
         return redirect('/register')

      user = User.objects.create(
         first_name = first_name,
         last_name = last_name,    username = username,
      )

      user.set_password(password)
      user.save()

      messages.info(request, 'Account created successfully')
      return redirect('/register')
   return render(request, 'register.html')


from django.db.models import Q,Sum

def get_students(request):
   queryset = Student.objects.all()

  


   if request.GET.get('search'):
      search=queryset.filter(Q(student_name__icontains = search) | Q(department__department__icontains = search) | Q (student_id__student_id__icontains = search) | Q(student_email__icontains = search) |Q
     (student_age__icontains = search)
                             )




   return render(request , 'report/students.html', {'queryset' : queryset})


def listing(request):
    queryset = Student.objects.all()
    paginator = Paginator(queryset, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page" , 1)
    page_obj = paginator.get_page(page_number)
    print (page_obj)
    return render(request, "report/students.html", {"queryset": page_obj})

from .seed import generate_report_card
def see_marks(request , student_id):
   #generate_report_card()
   queryset = SubjectMarks.objects.filter(student__student_id__student_id = student_id)
   total_marks= queryset.aggregate(total_marks = Sum('marks'))
   current_rank = -1

   ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks' , '-student_age')
   i=1

   for rank in ranks:
      if student_id == rank.student_id.student_id:
         current_rank=i
         break
      i=i+1
   
   return render(request , 'report/see_marks.html', {'queryset' : queryset , 'total_marks': total_marks , 'currrent_rank' : current_rank
   })


