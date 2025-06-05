from django.urls import path
from . import views

urlpatterns = [
    path('csrf', views.get_csrf_token),
    path('signup', views.SignupView.as_view()),
    path('login', views.LoginView.as_view()),
    path('me', views.MeView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('google-login/', views.GoogleLoginView.as_view()),
    path('merchant/signup/', views.MerchantSignupView.as_view()),
    path('forgot-password/', views.ForgotPasswordView.as_view()),
    path('reset-password/', views.ResetPasswordView.as_view()),
    
]
