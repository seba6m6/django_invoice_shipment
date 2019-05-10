from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.views import View
from photo.forms import UserForm, LoginForm
# Create your views here.



class UserFormView(View):

    class_form = UserForm
    template_name = 'registration_form.html'

    def get(self,request):
        form = self.class_form(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form = self.class_form(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('photo:main')
        return render(request, self.template_name, {'form':form})

class LoginFormView(View):
    class_form = LoginForm
    template_name ="accounts/login_form.html"

    def get(self,request):
        form = self.class_form(None)
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form=self.class_form(request.POST)
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('photo:main')

        error = "You did not enter a proper credentials"
        return render(request,'accounts/login_form.html', {'error': error} )

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return render(request,"main.html",{})