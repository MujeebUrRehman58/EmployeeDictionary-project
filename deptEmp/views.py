from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Department, Employee

@login_required
def home(request):
	emps = Employee.objects
	depts = Department.objects
	name, dept, email, man = '', '', '',None
	
	try:
		man = Employee.objects.get(manOfMonth = True)
	except:
		pass
	
	if man is not None:
		if request.method == 'POST':
			if request.POST['department']:
				if request.POST['department'] != 'All':
					dept = request.POST['department']
			if request.POST['fname']:
				name = request.POST['fname']
			if request.POST['email']:
				email = request.POST['email']
			
			emps = Employee.objects.filter(email__icontains = email, full_name__icontains = name, dept__dept_name__icontains = dept)
			context = {'email':email, 'name':name, 'dept':dept, 'emps':emps, 'depts':depts, 'man':man}
			return render(request, 'deptEmp/home.html', context)
				
		return render(request, 'deptEmp/home.html', {'emps':emps, 'depts':depts, 'man':man})
	else:
		return render(request, 'deptEmp/home.html', {'emps':emps, 'depts':depts, 'man':man})

@login_required
def emp_details(request, user_id):
	emp = get_object_or_404(Employee, pk=user_id)
	return render(request, 'deptEmp/emp_details.html', {'emp':emp })

@login_required
def create(request):
	users = User.objects
	depts = Department.objects

	context = {'name':'', 'username':'', 'email':'',
			   'title':'', 'department':'', 'level':'',
			   'cell':'', 'work':'', 'home':'',
			   'address':'', 'man':False,
	}

	rules = [request.POST.get('fname'),
		   request.POST.get('username'),
		   request.POST.get('email'),
		   request.POST.get('title'),
		   request.POST.get('department'),
		   request.POST.get('level'),
		   request.POST.get('cell phone'),
		   request.POST.get('home phone'),
		   request.POST.get('work phone'),
		   request.POST.get('address'),
		   request.FILES.get('profile'),
		   request.POST.get('password1'),
		   request.POST.get('password2'),
	]
	if request.POST.get('title') == 'Choose...':
		rules[3] = False
	if request.POST.get('department') == 'Choose...':
		rules[4] = False

	if rules[0]: context['name'] = request.POST['fname']
	if rules[1]: context['username'] = request.POST['username']
	if rules[2]: context['email'] = request.POST['email']
	if rules[3]: context['title'] = request.POST['title']
	if rules[4]: context['department'] = request.POST['department']
	if rules[5]: context['level'] = request.POST['level']
	if rules[6]: context['cell'] = request.POST['cell phone']
	if rules[7]: context['home'] = request.POST['home phone']
	if rules[8]: context['work'] = request.POST['work phone']
	if rules[9]: context['address'] = request.POST['address']
	if request.POST.get('man of month'): context['man'] = True

	if request.method == 'POST':
		if request.POST['password1'] == request.POST['password2']:
			if all(rules):
				try:
					user = User.objects.get(username=request.POST['username'])
					data = {'error':'Username already taken','depts':depts}
					return render(request, 'deptEmp/create.html', {**data, **context})
				except User.DoesNotExist:
					user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
				
					emp = Employee()
					emp.full_name = request.POST['fname']
					emp.user = user
					emp.email = request.POST['email']
					emp.title = request.POST['title']
					emp.dept = Department.objects.get(dept_name=request.POST['department'])
					emp.level = request.POST['level']
					emp.cell_phone = request.POST['cell phone']
					emp.home_phone = request.POST['home phone']
					emp.work_phone = request.POST['work phone']
					emp.address = request.POST['address']
					emp.profile = request.FILES['profile']
					if request.POST.get('man of month'):
						Employee.objects.update(manOfMonth=False)
						emp.manOfMonth = True
					else:
						emp.manOfMonth = False 
					emp.save()
					return redirect('/employee/' + str(emp.user.id))
			else:
				data = {'error':'All fields are required', 'depts':depts}
				return render(request, 'deptEmp/create.html', {**data, **context})
			
		else:
			print(str(request.POST['password1']))
			print(str(request.POST['password2']))
			data = {'error':'Passwords must match', 'depts':depts}
			return render(request, 'deptEmp/create.html', {**data, **context})

	return render(request, 'deptEmp/create.html', {'depts':depts})
