"""yuki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from users import views as user_views

def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='animals/home.html'), name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', next_page="login"), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('animals/', include('animals.urls', namespace='animals')),
    path('users/', include('users.urls', namespace='users')),
    path('schedules/', include('schedules.urls', namespace='schedules')),
    path('healthbook/', include('healthbook.urls', namespace='healthbook')),
    path('messenger/', include('messenger.urls', namespace="messenger")),
    path('friends/', include('friends.urls', namespace="friends")),
    path('autocomplete/', include('autocomplete.urls', namespace='autocomplete')),
    # path('notifications/', include('notifications.urls', namespace="notifications")),  
    path('sentry-debug/', trigger_error),
    ]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

