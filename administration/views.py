from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from deptEmp.models import Department, Employee

# Create your views here.
@login_required
def administration(request):
	return render(request, 'administration/administration.html')

@login_required
def departments(request):
	depts = Department.objects
	return render(request, 'administration/departments.html', {'depts':depts})

@login_required
def members(request):
	emps = Employee.objects
	name, username, man = '', '', None

	if request.method == 'POST':
		if request.POST['fname']:
			name = request.POST['fname']
		if request.POST['username']:
			username = request.POST['username']
		
		if request.POST["man of month"]:
			if request.POST["man of month"] == 'Yes':
				man = True
				emps = Employee.objects.filter(full_name__icontains = name, user__username__icontains = username, manOfMonth = True)

			elif request.POST["man of month"] == 'No':
				man = False
				emps = Employee.objects.filter(full_name__icontains = name, user__username__icontains = username, manOfMonth = False)
				
			else:
				emps = Employee.objects.filter(full_name__icontains = name, user__username__icontains = username)
		
		context = {'name':name, 'username':username, 'man':man, 'emps':emps}
		return render(request, 'administration/members.html', context)

	return render(request, 'administration/members.html', {'emps':emps})

@login_required
def editDept(request, dept_id):
	dept = get_object_or_404(Department, pk=dept_id)
	name = ''
	if request.method == 'POST':
		if request.POST['department']:
			if 'update' in request.POST:
				dept.dept_name = request.POST['department']
				dept.save()
				return redirect('departments')
			elif 'delete' in request.POST:
				dept.delete()
				return redirect('departments')
			else:
				return redirect('departments')		
	return render(request, 'administration/editDept.html', {'dept':dept})

@login_required
def insertDept(request):
	if request.method == 'POST':
		if request.POST['department']:
			try:
				dept = Department.objects.get(dept_name=request.POST['department'])
				return render(request, 'administration/insertDept.html', {'error':'Department already exists.'})
			except Department.DoesNotExist:
				dept = Department()
				dept.dept_name = request.POST['department']
				dept.save()
				return redirect('departments')
		else:
			return render(request, 'administration/insertDept.html', {'error':'Please enter department name.'})
			
	return render(request, 'administration/insertDept.html',)

@login_required
def editMem(request, id):
	mem = get_object_or_404(Employee, pk=id)
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
	]

	if request.POST.get('title') == 'Choose...':
		rules[3] = False
	if request.POST.get('department') == 'Choose...':
		rules[4] = False

	if request.method == 'POST':
		if 'update' in request.POST:
			if all(rules):

				mem.full_name = request.POST['fname']
				user = User.objects.get(pk=id)
				user.username = request.POST['username']
				user.save()
				mem.email = request.POST['email']
				mem.title = request.POST['title']
				mem.dept = Department.objects.get(dept_name=request.POST['department'])
				mem.level = request.POST['level']
				mem.home_phone = request.POST['home phone']
				mem.cell_phone = request.POST['cell phone']
				mem.work_phone = request.POST['work phone']
				mem.address = request.POST['address']
				if request.FILES.get('profile'):
					mem.profile = request.FILES['profile']
				if request.POST.get('man of month'):
					mem.manOfMonth = True
					Employee.objects.update(manOfMonth=False)
				else:
					mem.manOfMonth = False
				mem.save()
				return redirect('members')
			else:
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

				data = {'users':users, 'depts':depts, 'mem':mem, 'error':'All fields required.'}
				return render(request, 'administration/editMem.html', {**data, **context})
								
		elif 'delete' in request.POST:
			mem.delete()
			return redirect('members')
		else:
			return redirect('members')

	return render(request, 'administration/editMem.html', {'users':users, 'depts':depts, 'mem':mem})