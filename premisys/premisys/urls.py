"""premisys URL Configuration

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
from django.conf.urls         import url, include 
from apps_premisys.report.api.views import (
    employeeTourniquets,
    employeeSuspected,
    employeeFrecuent,
    employeeNumber,
    readTourniquets
)

from apps_premisys.merakiNetwork.api.views import (
    merakiOrganizations,
    merakiNetworks,
    merakiDevices,
    merakiClient,
    get_network_clients_connection_stats,
    get_network_ssids
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/employeeTourniquets/$', employeeTourniquets.as_view(), name="url"),
    url(r'^api/v1/employeeSuspected/$', employeeSuspected.as_view(), name="url"),
    url(r'^api/v1/employeeFrecuent/', employeeFrecuent.as_view(), name="url"),
    url(r'^api/v1/employeeNumber/', employeeNumber.as_view(), name="url"),
    url(r'^api/v1/merakiOrganizations/$', merakiOrganizations.as_view(), name="url"),
    url(r'^api/v1/readTourniquets/', readTourniquets.as_view(), name="url"),
    path('api/v1/merakiNetworks/<int:pk>/', merakiNetworks.as_view()),
    path('api/v1/merakiDevices/<str:pk>/', merakiDevices.as_view()),
    path('api/v1/merakiClient/<str:pk>/', merakiClient.as_view(), name="url"),
    path('api/v1/get_network_clients_connection_stats/', get_network_clients_connection_stats.as_view(), name="url"),
    path('api/v1/get_network_ssids/', get_network_ssids.as_view(), name="url")
    
]
