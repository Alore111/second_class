"""
URL configuration for ulb_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from backend.views import login
from backend.views import sc_data
from backend.views import choose
from backend.views import register_data
from backend.views import register
from backend.views import basin_data
from backend.views import img
from django.urls import path
from backend import views

urlpatterns = [
    path('login/login', login, name='login'),
    path('choose/sc_data', sc_data, name='sc_data'),
    path('choose/choose', choose, name='choose'),
    path('my_sc/register_data', register_data, name='register_data'),
    path('my_sc/register', register, name='register'),
    path('personal/basin_data', basin_data, name='basin_data'),
    path('personal/img', img, name='img'),
    path('images/get', views.get_image, name='get_image'),
]



