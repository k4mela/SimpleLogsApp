from rest_framework import serializers
from .models import AddLogs

class AddLogsSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    sevlevel = serializers.IntegerField()
    time = serializers.DateTimeField()
    projname = serializers.CharField()
    logcont = serializers.CharField()

    class Meta:
        model = AddLogs
        fields = ('__all__')