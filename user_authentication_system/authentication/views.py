from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from user_authentication_system import settings

# Create your views here.


def index(request):
    return render(request, "authentication/index.html")

def signup(request):


    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']    

        if User.objects.filter(username=username):
            messages.error(request, "This user is already exist, please try other username")
            return redirect("home")
        
        if User.objects.filter(email=email):
            messages.error(request, "This email is already exist, please try other email")

        if pass1 != pass2:
            messages.error(request, "The password did not match!")

        if not username.isalnum():
            messages.error(request, " The username must be Alpha-Numeric")
            return redirect("home")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()

        messages.success(request, "Your account has been created successfully")

        subject = "Welcome to Micron Technologies - Django Login "
        message = "Hello" + myuser.first_name + "!! \n " + "Welcome to Micron Technologies!! \n Thank you for visiting our website \n We have sent you a confirmation email, Please confirm your email address inorder to activate your account. Thank you \n\n Muhammed adil" 
        from_mail = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_mail, to_list, fail_silently=True)

        return redirect("signin") 


    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']


        user = authenticate(username=username, password=pass1, )

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname':fname})
        
        else:
            messages.error(request, "Bad credentials!")
            return redirect('home')
        

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Your are successfully logged out!!")
    return redirect('home')