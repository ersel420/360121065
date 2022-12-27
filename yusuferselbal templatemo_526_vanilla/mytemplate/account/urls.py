from django.urls import path
from . import views
from django.contrib.auth import views as authViews
from django.views.generic import TemplateView
from .forms import UserLoginForm, PwdResetForm, PwdResetConfirmForm

app_name = 'account'

urlpatterns = [
    #Register
    path('register/', views.accountRegister, name = 'register'),
    path('activate/<slug:uidb64>/<slug:token>', views.accountActivate, name = 'activate'),
    path('dashboard', views.dashboard, name = 'dashboard'),

    #Login / Logout
    path('login', authViews.LoginView.as_view(
        template_name = 'account/registration/login.html', 
        form_class = UserLoginForm), name = 'login'),
    path('logout', authViews.LogoutView.as_view(
        next_page = '/account/login'), name = 'logout'),

    #Profile Changes
    path('profile/edit/', views.editUser, name = 'edit'),
    path('profile/delete/', views.deleteUser, name = 'delete'),
    path('profile/delete-confirm/', TemplateView.as_view(
        template_name = 'account/user/delete-confirm.html'), name = 'deleteConfirm'),
    
    #Password Reset
    path('password_reset/', authViews.PasswordResetView.as_view(
        template_name = 'account/user/password_reset_form.html', 
        success_url = 'password_reset_email_confirm/', 
        email_template_name = 'account/user/password_reset_email.html', 
        form_class = PwdResetForm), name = 'pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', authViews.PasswordResetConfirmView.as_view(
        template_name = 'account/user/password_reset_confirm.html', 
        success_url = '/account/password_reset_complete/', 
        form_class = PwdResetConfirmForm), name = 'password_reset_confirm'),
    path('password_reset/password_reset_email_confirm/', TemplateView.as_view(
        template_name = 'account/user/reset_status.html',
    ), name = 'password_reset_done'),
    path('password_reset_complete/', TemplateView.as_view( #authViews.PasswordResetCompleteView
        template_name = 'account/user/reset_status.html',
    ), name = 'password_reset_complete'),

]
