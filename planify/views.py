import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from planify.forms import LoginForm, UserRegistrationForm, CreateTaskForm, TaskEditForm
from planify.models import Task
from utils.constants import WEEK_IN_DAYS


def base_page(request):
    return render(request, 'base.html')


def create_task(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            user_task = form.save(commit=False)
            user_task.task_owner = request.user
            user_task.save()
            return redirect('all_tasks')
        else:
            print(form.errors)
    else:
        form = CreateTaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})


def get_user_tasks(request):
    all_user_tasks = Task.objects.filter(task_owner=request.user).exclude(
        task_status=Task.Status.COMPLETED,
        task_updated_at__lte=datetime.datetime.now() - datetime.timedelta(days=WEEK_IN_DAYS),
    ).order_by('task_status', '-task_due_date')

    tasks_by_status = {status: [] for status, _ in Task.Status.choices}
    for task in all_user_tasks:
        tasks_by_status[task.task_status].append(task)

    columns = []
    for status, label in Task.Status.choices:
        columns.append({
            'code': status,
            'label': label,
            'tasks': tasks_by_status[status],
        })

    return render(request, 'tasks/get_user_tasks.html', {
        'columns': columns,
    })


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, task_owner=request.user)

    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=pk)
    else:
        form = TaskEditForm(instance=task)

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'form': form,
    })


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Вы успешно аунтентифицировались!')
                else:
                    return HttpResponse('Аутентификация не прошла!')
            else:
                return HttpResponse('Невалидный аккаунт!')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(
                request,
                'registration/register_done.html',
                {'new_user': new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'registration/register.html',
        {'user_form': user_form},
    )
