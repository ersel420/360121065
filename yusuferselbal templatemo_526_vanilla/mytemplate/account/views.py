from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import accountActivationToken
from .models import UserBase
from .forms import RegistrationForm, UserEditForm

# Create your views here.

@login_required
def dashboard(request): #Dashboard
    return render(request, 'account/user/dashboard.html')
        
def accountRegister(request): #Register
    if request.user.is_authenticated:
        return redirect('website:home')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            currentSite = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/acc-activation-email.html', {
                'user': user,
                'domain': currentSite.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': accountActivationToken.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/acc-activation-sent.html')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {
        'form': registerForm,
    })


def accountActivate(request, uidb64, token): #Activate Account
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and accountActivationToken.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('website:home')
    else:
        return render(request, 'account/registration/acc-activation-invalid.html')


@login_required
def editUser(request): #Edit User Info
    if request.method == 'POST':
        userForm = UserEditForm(instance = request.user, data = request.POST)
        if userForm.is_valid():
            userForm.save()
    else:
        userForm = UserEditForm(instance = request.user)
    
    return render(request, 'account/user/profile.html', {
        'userForm': userForm,
    })

@login_required
def deleteUser(request): #Delete User from Database (Actually, set is_active = False)
    user = UserBase.objects.get(user_name = request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:deleteConfirm')
    