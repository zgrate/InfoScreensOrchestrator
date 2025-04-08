"""
URL configuration for InfosystemOrchestrator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

import screen.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('screen/<str:passphrase>/', screen.views.screen_view),
    path('generate/<str:name>/', screen.views.generate_screen),
    path('switch_group/<str:access_token>/<int:group>/<int:new_command>', screen.views.switch_command_group),
    path('switch_screen/<str:access_token>/<int:screen_id>/<int:new_command>', screen.views.switch_command_screen),
    path('switch_screen_override/<str:access_token>/<int:screen_id>/', screen.views.switch_screen_override),
    path('screen_info/<str:access_token>/<int:screen_id>/', screen.views.screen_info),
    path('screen_group_info/<str:access_token>/<int:screen_group_id>/', screen.views.screen_group_info),
    path('metrics/', screen.views.metrics)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

