from django.db import models


class Resource(models.Model):
    STATUS = (('billable', 'Billable'), ('available', 'Available'), ('assigned', 'Assigned'))
    name = models.CharField(max_length=100)
    technology = models.CharField(max_length=100)
    status = models.CharField(max_length=20,choices=STATUS,default = 'available')
    start_date = models.DateField(null=True, blank = True)
    end_date = models.DateField(null=True, blank = True)
    project = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
