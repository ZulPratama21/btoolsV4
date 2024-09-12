from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def loginView(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	if request.method == "POST":
		username_login = request.POST['username']
		password_login = request.POST['password']

		user = authenticate(request, username=username_login, password=password_login)

		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			pass

	return render(request, 'login.html')

@login_required(redirect_field_name='next', login_url='/login')
def dashboard(request):
	return render(request, 'dashboard.html')
