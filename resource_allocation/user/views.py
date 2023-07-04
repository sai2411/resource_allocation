from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.http import JsonResponse
from datetime import date, timedelta
from .models import Resource
def index(request):
    return render(request, 'user/index.html', {'title': 'Resource Allocation'})

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error occurred while processing the registration form.')
    else:
        form = NewUserForm()
    return render(request, 'user/register.html', {'form': form, 'title': 'Register'})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('index')  
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form, 'title': 'Login'})


@login_required
def profile(request):
    if request.method == 'POST':
        resource_name = request.POST.get('resource_name')
        resource_technology = request.POST.get('resource_technology')
        if resource_name and resource_technology:
            resource = Resource.objects.create(
                name = resource_name,
                technology = resource_technology
            )
            return redirect('resource-list')
    else:
        return render(request, 'user/profile.html', {'title': 'Resource Allocation'})
def update_resource_status(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    status = request.POST.get('status')
    if status == 'assigned':
        start_date = resource.project.start_date
        days_until_start = (start_date - date.today()).days
        if days_until_start > 7:
            return JsonResponse({'success': False, 'message': 'The project allocation is allowed only if the project starts within 7 days.'})
    if status == 'assigned' and resource.status != 'assigned':
        resource.status = status
        resource.save()
        resource.status = 'billable' if resource.project.start_date == date.today() else 'assigned'
    else:
        resource.status = status
        resource.save()

    return JsonResponse({'success': True})
