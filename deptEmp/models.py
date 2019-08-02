from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Department(models.Model):
	dept_name = models.CharField(max_length=255)

	def __str__(self):
		return self.dept_name

class Employee(models.Model):
	full_name = models.CharField(max_length=200)
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	email = models.EmailField(max_length=70)
	title = models.CharField(max_length=255)
	dept = models.ForeignKey(Department, on_delete=models.CASCADE)
	level = models.CharField(max_length=255)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	cell_phone = models.CharField(validators=[phone_regex], max_length=17)
	home_phone = models.CharField(validators=[phone_regex], max_length=17, null=True)
	work_phone = models.CharField(validators=[phone_regex], max_length=17, null=True)
	address = models.CharField(max_length=1024, null=True)
	manOfMonth = models.BooleanField(default=False, null=True)
	profile = models.ImageField(upload_to="images/")	

	def __str__(self):
		return self.full_name