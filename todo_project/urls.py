"""
URL configuration for todo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from todo.views import (
    home,
    delete_task,
    complete_task,
    edit_task,
    clear_completed,
    register,
    login_view,
    logout_view,
)


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('register/', register, name='register'),

    path('login/', login_view, name='login'),

    path('logout/', logout_view, name='logout'),

    path(
        'delete/<int:task_id>/',
        delete_task,
        name='delete_task'
    ),

    path(
        'complete/<int:task_id>/',
        complete_task,
        name='complete_task'
    ),

    path(
        'edit/<int:task_id>/',
        edit_task,
        name='edit_task'
    ),

    path(
        'clear-completed/',
        clear_completed,
        name='clear_completed'
    ),
]