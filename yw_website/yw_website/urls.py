"""yw_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings as conf_settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

urlpatterns = [
    ###
    # USER PATHS
    ###
    path('admin/', admin.site.urls,),
    path('accounts/', include('allauth.urls')),
    path('search/', include('haystack.urls'), name='haystack_search'),
    path('', include('yw_website.apps.website.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls'))
]

if conf_settings.DEBUG:
    urlpatterns += static(website_settings.MEDIA_URL,
                          document_root=website_settings.MEDIA_ROOT)
