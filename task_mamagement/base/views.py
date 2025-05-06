from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperAdmin, IsAdmin
from .models import Task, User
from .serializers import TaskSerializer
from .decorators import superadmin_required, admin_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
# Create your views here.

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)

        if request.data.get("status") == "completed":
            task.status = "completed"
            task.completion_report = request.data.get("completion_report", "")
            task.worked_hours = request.data.get("worked_hours", 0)
            if task.completion_report and task.completion_report:
                task.save()
                return Response({'message': 'Task marked as completed'})
            else:
                return Response({'error': 'Completion report and worked hours is required'})
        return Response({'error': 'Invalid status update'}, status=400)


class TaskReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        # if request.user.role not in ['admin', 'superadmin']:
        #     return Response({'error': 'Not authorized'}, status=403)
        try:
            task = Task.objects.get(pk=pk, status='completed')
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)

        data = {
            'title': task.title,
            'assigned_to': task.assigned_to.username,
            'completion_report': task.completion_report,
            'worked_hours': task.worked_hours,
        }
        return Response(data)



def admin_panel(request):
    if not request.user.is_authenticated:
        return redirect('login-page')
    if request.user.role == 'user':
        users = User.objects.none()
        tasks = Task.objects.filter(assigned_to= request.user)
    elif request.user.role == 'admin':
        users = User.objects.filter(assigned_to= request.user)
        tasks = Task.objects.filter(assigned_to__assigned_to= request.user)
    else:
        users = User.objects.all()
        tasks = Task.objects.all()
    context = {
        'users': users,
        'tasks': tasks
    }
    return render(request, "admin_panel.html", context)
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('admin-panel')
        messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

@superadmin_required
def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully!')
            return redirect('admin-panel')
    else:
        form = UserCreationForm()
        form.fields['assigned_to'].queryset = User.objects.filter(role= 'admin')
    return render(request, 'add_user.html', {'form': form})

@superadmin_required
def edit_user(request, pk):
    user = User.objects.get(pk= pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance= user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully!')
            return redirect('admin-panel')
    else:
        form = UserEditForm(instance= user)
        form.fields['assigned_to'].queryset = User.objects.filter(role= 'admin')
    return render(request, 'add_user.html', {'form': form})

@superadmin_required
def promote_user(request, pk):
    user = User.objects.get(pk= pk)
    if user.role == 'admin':
        user.role = 'superadmin'
    elif user.role == 'user':
        user.role = 'admin'
    user.save()
    return redirect('admin-panel')

@superadmin_required
def demote_user(request, pk):
    user = User.objects.get(pk= pk)
    if user.role == 'admin':
        user.role = 'user'
    user.save()
    return redirect('admin-panel')

@superadmin_required
def delete_user(request, pk):
    User.objects.get(pk= pk).delete()
    return redirect('admin-panel')


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully!')
            return redirect('admin-panel')
    else:
        form = TaskForm()
        form.fields['assigned_to'].queryset = User.objects.filter(role= 'user', assigned_to= request.user)
    return render(request, 'add_task.html', {'form': form})


def edit_task(request, pk):
    task = Task.objects.get(pk= pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance= task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('admin-panel')
    else:
        form = TaskForm(instance= task)
        form.fields['assigned_to'].queryset = User.objects.filter(role= 'user', assigned_to= request.user)
    return render(request, 'add_task.html', {'form': form})


def delete_task(request, pk):
    Task.objects.get(pk= pk).delete()
    return redirect('admin-panel')


def logout_view(request):
    logout(request)
    return redirect('login-page')