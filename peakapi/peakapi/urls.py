"""peakapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from .views import login, sample_api
from goals.views import get_goals, post_goal, post_goal_challenge, post_user_goal_attempt, get_goal_challenges

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('sampleapi/', sample_api),
    path('goals/', get_goals),
    path('goal/', post_goal),
    path('challenge/', post_goal_challenge),
    path('challenges/', get_goal_challenges),
   	path('goal/attempt/<int:id>', post_user_goal_attempt),
]
