from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import bcrypt
import re


from .models import UnsafeUser

def index(request):
    return HttpResponseRedirect(reverse("login"))

class ProfileView(View):
    def get(self, request):
        print(request.user)
        return render(request, "users/profile.html", {"user": request.user})
    
    def post(self, request):
        pass
        # TODO: update profile description

class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_encoded = password.encode("utf-8")
        try:
            user = UnsafeUser.objects.get(username=username)
        except UnsafeUser.DoesNotExist:
            return render(request, "users/login.html", {"error": "Wrong username or password."})
        
        # Login checks for either a plaintext password or crypted one, so that the fixing vulnerability 2 can be demonstrated.
        if password_encoded == user.password_hash or bcrypt.checkpw(password_encoded, user.password_hash):
            print("passwords match!")
            request.session["user"] = user.username
            return HttpResponseRedirect(reverse("profile"))
        else:
            print("password wrong!")
            return render(request, "users/login.html", {"error": "Wrong username or password."})


class SignupView(View):
    def get(self, request):
        return render(request, "users/signup.html")
    
    def strong_password(self, password):
        long_enough = len(password) > 7
        lowercase = re.search("[a-z]", password)
        uppercase = re.search("[A-Z]", password)
        numbers = re.search("[0-9]", password) 

        # vulnerability 1: Weak passwords can be used. https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
        # return True
        # vulnerability 1 is fixed by requiring passwords to be complex enough.
        return long_enough and lowercase and uppercase and numbers

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")
        
        if not username or not password:
            return render(request, "users/signup.html", {"error": "Missing username or password."})
        if password != password_confirmation:
            return render(request, "users/signup.html", {"error": "Passwords don't match."})
        
        if self.strong_password(password):
            # vulnerability 2: Passwords are stored as plain text. https://owasp.org/Top10/A04_2021-Insecure_Design/
            password_hash = password.encode("utf-8")
            # vulnerability 2 is fixed by crypting passwords properly
            # password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            UnsafeUser.objects.create(username=username, password_hash=password_hash)
            
            return render(request, "users/login.html", {"success": "Account created succesfully! Login with your credentials."})
        else:
            return render(request, "users/signup.html", {"error": "Password must be atleast 8 characters long and contain numbers, lowercase and uppercase characters."})
        

    
# logout
# session tyhjäys
# request.session.flush() 