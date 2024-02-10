# urls.py
from django.urls import path
from vele import views

urlpatterns = [
    path('', views.home, name='home'),  # Assuming 'home' is the view for the home page
    path('process_form/', views.process_form, name='process_form'),
]
