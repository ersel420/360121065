from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import UserBase
from .forms import RegistrationForm, UserEditForm
from .tokens import accountActivationToken
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'website/home.html')
        
def accountRegister(request):

    # if request.user.is_authenticated:
    #     return redirect('account:dashboard')

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
            return HttpResponse('Registered Succesfully and Activation is Sent to Mail Address.')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def accountActivate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and accountActivationToken.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/acc-activation-invalid.html')


@login_required
def editUser(request):
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
def deleteUser(request):
    user = UserBase.objects.get(user_name = request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:deleteConfirm')
    