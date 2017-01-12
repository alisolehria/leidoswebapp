from django.contrib import admin
from adminUser.models import location

class locationAdmin(admin.ModelAdmin):
    list_display = ('locationID', 'country', 'city')

admin.site.register(location, locationAdmin)

