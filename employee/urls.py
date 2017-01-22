from django.conf.urls import url
from . import views

app_name = "employee"

urlpatterns = [
    url(r'alerttab/$', views.alerttab_View, name='alertTab'),
    url(r'profile/$', views.profile_View, name='profile'),
    url(r'myprojects/$', views.myprojects_View, name='myprojects'),
    url(r'projectlist/$', views.projectlist_View, name='projectlist'),
    url(r'currentProjects/$', views.currentprojectsget_View, name='currentprojectsget'),
    url(r'upcomingProjects/$', views.upcomingprojectsget_View, name='upcomingprojectsget'),
    url(r'completedProjects/$', views.completedprojectsget_View, name='completedprojectsget'),
    url(r'project/$', views.projectprofile_View, name='projectprofile'),
    url(r'staff/$', views.staffprofile_View, name='staffprofile'),
    url(r'alerts/$', views.alert_View, name='alerts'),
    url(r'requestholiday/$', views.holiday_View, name='holidayrequest'),


]