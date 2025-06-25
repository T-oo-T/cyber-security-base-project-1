from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
import bcrypt
import re


from .models import UnsafeUser, UserAudit

def index(request):
    return HttpResponseRedirect(reverse("login"))

class ProfileView(View):
    def get(self, request, user_id):
        if not request.session.get("user_id"):
            return HttpResponseRedirect(reverse("login"))
        
        # vulnerability 3: not checking that the currently logged in user can access the profile at url /profile/<user_id>
        # https://owasp.org/Top10/A01_2021-Broken_Access_Control/
        # vulnerability 3 is fixed by checking that the user defined in the url is the same as the logged in user
        # if request.session.get("user_id") != user_id:
        #    return HttpResponseForbidden()
            
        user = UnsafeUser.objects.get(pk=user_id)
        return render(request, "users/profile.html", {"user": user})
        
    def post(self, request, user_id):
        user = UnsafeUser.objects.get(pk=user_id)
        new_description = request.POST.get("description")
        
        user.description = new_description
        user.save()

        return HttpResponseRedirect(reverse("profile", args=(user.id,)))

class LogoutView(View):
    def post(self, request):
        request.session.flush()
        return HttpResponseRedirect(reverse("login"))

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
            request.session["user_id"] = user.id
            # vulnerability 5: user logins are not logged, https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
            # vulnerability 5 is fixed by logging user logins
            # ideally all actions should be logged, logging only the login is done here for keeping the example simple.
            # UserAudit.objects.create(user_id=user)
            return HttpResponseRedirect(reverse("profile", args=(user.id,)))
        else:
            return render(request, "users/login.html", {"error": "Wrong username or password."})


class SignupView(View):
    def get(self, request):
        return render(request, "users/signup.html")
    
    def strong_password(self, password):
        long_enough = len(password) > 7
        lowercase = re.search("[a-z]", password)
        uppercase = re.search("[A-Z]", password)
        numbers = re.search("[0-9]", password) 
        special = re.search("[^\w]", password)

        # vulnerability 1 is fixed by requiring passwords to be complex enough.
        # return long_enough and lowercase and uppercase and numbers and special

        # vulnerability 1: Weak passwords can be used. https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
        return True
        
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
            return render(request, "users/signup.html", {"error": "Password must be atleast 8 characters long and contain special characters, numbers, lowercase and uppercase characters."})