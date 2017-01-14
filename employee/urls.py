from django.conf.urls import url
from . import views

app_name = "employee"

urlpatterns = [
    url(r'alerttab/$', views.alerttab_View, name='alertTab'),
    url(r'profile/$', views.profile_View, name='profile'),

]