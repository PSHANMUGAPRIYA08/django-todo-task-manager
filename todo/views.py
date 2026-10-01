from django.shortcuts import render, redirect
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Task


@login_required
def home(request):

    if request.method == 'POST':

        title = request.POST['title']
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        Task.objects.create(
            user=request.user,
            title=title,
            due_date=due_date if due_date else None,
            priority=priority
        )

        return redirect('home')

    tasks = Task.objects.filter(user=request.user)

    today = timezone.now().date()

    total_tasks = Task.objects.filter(
        user=request.user
    ).count()

    completed_tasks = Task.objects.filter(
        user=request.user,
        completed=True
    ).count()

    active_tasks = Task.objects.filter(
        user=request.user,
        completed=False
    ).count()

    search = request.GET.get('search')

    if search:
        tasks = tasks.filter(
            title__icontains=search
        )

    filter_type = request.GET.get('filter')

    if filter_type == 'active':
        tasks = tasks.filter(
            completed=False
        )

    elif filter_type == 'completed':
        tasks = tasks.filter(
            completed=True
        )

    sort_type = request.GET.get('sort')

    if sort_type == 'due_date':

        tasks = tasks.order_by('due_date')

    elif sort_type == 'priority':

        tasks = tasks.order_by(
            models.Case(
                models.When(priority='High', then=1),
                models.When(priority='Medium', then=2),
                models.When(priority='Low', then=3),
            )
        )

    return render(
        request,
        'todo/home.html',
        {
            'tasks': tasks,
            'search': search,
            'filter_type': filter_type,
            'total_tasks': total_tasks,
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks,
            'today': today,
            'sort_type': sort_type,
        }
    )


@login_required
def delete_task(request, task_id):

    task = Task.objects.get(
        id=task_id,
        user=request.user
    )

    task.delete()

    return redirect('home')


@login_required
def complete_task(request, task_id):

    task = Task.objects.get(
        id=task_id,
        user=request.user
    )

    task.completed = not task.completed
    task.save()

    return redirect('home')


@login_required
def edit_task(request, task_id):

    task = Task.objects.get(
        id=task_id,
        user=request.user
    )

    if request.method == 'POST':

        task.title = request.POST['title']
        task.due_date = request.POST.get('due_date') or None
        task.priority = request.POST.get('priority')

        task.save()

        return redirect('home')

    return render(
        request,
        'todo/edit.html',
        {'task': task}
    )


@login_required
def clear_completed(request):

    if request.method == 'POST':

        Task.objects.filter(
            user=request.user,
            completed=True
        ).delete()

    return redirect('home')


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:

            return render(
                request,
                'todo/register.html',
                {'error': 'Passwords do not match.'}
            )

        if User.objects.filter(username=username).exists():

            return render(
                request,
                'todo/register.html',
                {'error': 'Username already exists.'}
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(
        request,
        'todo/register.html'
    )


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        return render(
            request,
            'todo/login.html',
            {'error': 'Invalid username or password.'}
        )

    return render(
        request,
        'todo/login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('login')