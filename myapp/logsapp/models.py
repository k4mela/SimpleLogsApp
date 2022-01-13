from django.db import models

class AddLogs(models.Model):
    user = models.CharField(max_length=10)
    sevlevel = models.IntegerField()
    time = models.DateTimeField()
    projname = models.CharField(max_length=50)
    logcont = models.CharField(max_length=50)
    

class AddProjects(models.Model):
    user = models.CharField(max_length=10)
    project = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
