from django.urls import path
from . import views 
urlpatterns = [
    path('', views.home, name='home'),
    path('employee/<int:user_id>', views.emp_details, name='emp_details'),
    path('employee/create', views.create, name='create'),
]