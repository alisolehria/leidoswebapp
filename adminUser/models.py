from django.db import models

class location(models.Model):
    class Meta:
        db_table = 'location'

    locationID = models.AutoField(primary_key=True)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    def __str__(self):
        return  self.city + ", " + self.country




