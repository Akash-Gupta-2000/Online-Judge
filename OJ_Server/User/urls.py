from django.urls import include, path
from . import views

urlpatterns = [
    path('register/', views.register, name = 'Register'),
    path('login/', views.login, name = 'Login'),
    path('logout/', views.logout, name = 'Logout'),
    # path('activate/<str:uidb64>/<str:token>',
    #      views.ActivateUserMethod, name='Account Verification'),
    path('getProfile/', views.getProfile, name ='User Profile'),
]