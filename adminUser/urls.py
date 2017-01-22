from django.conf.urls import url
from . import views

app_name = "adminUser"
urlpatterns = [
        url(r'dashboard/$', views.dashboard_View, name='dashboard'),
        url(r'stafflist/$', views.stafflist_View, name='stafflist'),
        url(r'projectlist/$', views.projectlist_View, name='projectlist'),
        url(r'currentStaff/$', views.currentstaff_View, name='currentstaff'),
        url(r'currentProjects/$', views.currentprojects_View, name='currentprojects'),
        url(r'upcomingProjects/$', views.upcomingprojects_View, name='upcomingprojects'),
        url(r'staff/(?P<staff_id>[0-9]+)/$',views.staffprofile_View, name='staffprofile'),
        url(r'currentProjects/(?P<staff_id>[0-9]+)/$', views.currentprojectsget_View, name='currentprojectsget'),
        url(r'upcomingProjects/(?P<staff_id>[0-9]+)/$', views.upcomingprojectsget_View, name='upcomingprojectsget'),
        url(r'completedProjects/(?P<staff_id>[0-9]+)/$', views.completedprojectsget_View, name='completedprojectsget'),
        url(r'project/(?P<project_id>[0-9]+)/$', views.projectprofile_View, name='projectprofile'),
        url(r'table/$', views.table_View, name='tableview'),
        url(r'addstaff/$', views.addstaff_View, name='addstaff'),
        url(r'addskill/(?P<staff_id>[0-9]+)/$', views.addskill_View, name='addskill'),
        url(r'addproject/$', views.addproject_View, name='addproject'),
        url(r'addpskill/(?P<project_id>[0-9]+)/$', views.addpskill_View, name='addpskill'),
        url(r'projectmembers/(?P<project_id>[0-9]+)/$', views.addpstaff_View, name='addpstaff'),
        url(r'skill/$', views.skill_View, name='skill'),
        url(r'location/$', views.location_View, name='location'),
        url(r'editprofile/(?P<staff_id>[0-9]+)/$', views.editprofile_View, name='editprofile'),
        url(r'edit/(?P<project_id>[0-9]+)/$', views.editproject_View, name='editproject'),
        url(r'alerts/$', views.alert_View, name='alerts'),
        url(r'alerttab/$', views.alerttab_View, name='alertTab'),
        url(r'requests/$', views.requests_View, name='requests'),
        url(r'requestholiday/$', views.holiday_View, name='holidayrequest'),
        url(r'report/(?P<project_id>[0-9]+)/$', views.report_View, name='report'),
]
