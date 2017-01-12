from django.contrib import admin
from . import models


class profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'staffID', 'dateOfBirth', 'nationality', 'preferredLocation' , 'gender', 'designation', 'workStatus', 'skillLevel','salary')

class workplaceView(admin.ModelAdmin):
    list_display = ('companyName', 'staffID', 'companyRating')

class projectView(admin.ModelAdmin):
    list_display = ('projectID', 'projectName', 'projectManager', 'location' , 'startDate', 'endDate', 'description', 'budget','numberOfStaff','status')

admin.site.register(models.previousWorkplaces, workplaceView)
admin.site.register(models.profile, profileAdmin)
admin.site.register(models.projects,projectView)
admin.site.register(models.skills)
admin.site.register(models.projectsWithSkills)
admin.site.register(models.staffWithSkills)
admin.site.register(models.holidays)
admin.site.register(models.alerts)
admin.site.register(models.staffAlerts)

