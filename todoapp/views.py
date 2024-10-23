from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

# @login_required
# def home(request):
#     if request.method == 'POST':
#         task = request.POST['task']
#         new_task = Task(user=request.user, task=task)
#         new_task.save()
        
#     all_tasks = Task.objects.filter(user=request.user)
#     context = {
#         'all_tasks': all_tasks
#     }
#     return render(request, 'home.html', context)

# Code for pagination is here
@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST['task']
        new_task = Task(user=request.user, task=task, is_deleted=False)
        new_task.save()
        
    # all_tasks = Task.objects.filter(user=request.user)
    # Handling search query
    query = request.GET.get('q')
    if query:
        all_tasks = Task.objects.filter(user=request.user, task__icontains=query,is_deleted=False).order_by('-created_at')
    else:
        all_tasks = Task.objects.filter(user=request.user, is_deleted=False).order_by('-created_at')
        

    # Pagination setup
    paginator = Paginator(all_tasks, 6)
    page = request.GET.get('page')
    
    try:
        tasks = paginator.page(page)
        print(tasks)
    except PageNotAnInteger:
        tasks = paginator.page(1) 
        print(tasks)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
        print(tasks)

    context = {
        'tasks': tasks
    }
    return render(request, 'alignment.html', context)

def signup(request):
    # if request.user.is_authenticates:
    #     return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # username validation   
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken. Please choose another.')
            return redirect('signup')
        
        # email validation
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists. Please log in or use a different email.")
            return redirect('signup')

        # password validation
        if len(password)<5:
            messages.error(request, "Password must be include more than 5 characters")
            return redirect('signup')
        
        # email validation
        if '@' not in email or '.' not in email.split('@')[-1]:
            messages.error(request, "Please enter a valid email address.")
            return redirect('signup')   
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        
        messages.success(request, "Your account has been created successfully. Please log in.")
        return redirect('signin')
        
        
    return render(request, 'signup.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'User logged successfully')
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('signin')
    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def FinishTask(request, id):
    # get_task_to_delete = Task.objects.get(request.user, task=name)
    get_task = get_object_or_404(Task, user=request.user, id=id)
    get_task.status = True
    get_task.save()
    messages.success(request, 'Task finished successfully!')
    return redirect('home')

@login_required
def UpdateTask(request, id):
    task_instance = get_object_or_404(Task, user=request.user, id=id)

    if request.method == 'POST':
        task_instance.task = request.POST['task']
        task_instance.status = request.POST['status']
        task_instance.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('home')

    context = {
        'task': task_instance
    }
    return render(request, 'update.html', context)

# @login_required
# def DeleteTask(request, id):
#     # get_task = Task.objects.get(request.user, task=name)
#     # get_task_to_delete = Task.objects.get(request.user, task=name)
#     get_task_to_delete = get_object_or_404(Task, user=request.user, id=id)
#     get_task_to_delete.delete()
#     messages.success(request, 'Task deleted successfully!')
#     return redirect('home')

@login_required
def DeleteTask(request, id):
    # get_task = Task.objects.get(request.user, task=name)
    get_task_to_delete = get_object_or_404(Task, user=request.user, id=id)
    get_task_to_delete.is_deleted = True
    get_task_to_delete.save()
    messages.success(request, 'Task deleted successfully!')
    return redirect('home')


