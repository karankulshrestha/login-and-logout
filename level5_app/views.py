from django.shortcuts import render
from level5_app.forms import UserProfileInfoForm, UserForm

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'basic_app/index.html', context=None)

@login_required
def special(request):
    return HttpResponse("You, are logged in | Nice")



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def registration(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        if user_form.is_valid() & profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()

            registered = True

        else:
            print('user_form.erros, profile_forms.errors')
        
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request, 'basic_app/registration.html', context={'registered':registered,
                                                                    'user_form':user_form,
                                                                    'profile_form':profile_form})





def user_login(request):
     
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password) 

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse("Accounts not active!")
        
        else:
            print("Someone Try To Login And fails !")
            print("username: {} and password: {}".format(username, password))

            return HttpResponse("Invalid login detials supplied!")
        
    else:
        return render(request, 'basic_app/login.html', {})