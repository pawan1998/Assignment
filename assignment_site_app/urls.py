from django.conf.urls import url
from assignment_site_app import views

urlpatterns = [
    url('pageone/', views.pageone, name='pageone'),
    # url('pagethree/', views.pagethree, name='pagethree'),
    url('registerpage/', views.registerPage, name='registerpage'),
    url('loginpage/', views.loginPage, name='loginpage'),
    url('logout/', views.logoutUser, name='logout')
]