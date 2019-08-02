from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.administration, name='administration'),
    path('departments/', views.departments, name='departments'),
    path('members/', views.members, name='members'),
    path('members/edit/<int:id>', views.editMem, name='editMem'),
    path('departments/edit/<int:dept_id>', views.editDept, name='editDept'),
    path('departments/insert', views.insertDept, name='insertDept'),

]