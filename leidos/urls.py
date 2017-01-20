from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^adminSite/', admin.site.urls),
    url(r'^', include('accounts.urls')),
    url(r'^admin/', include('adminUser.urls')),
    url(r'^pm/', include('projectManager.urls')),
    url(r'^employee/', include('employee.urls')),
]
