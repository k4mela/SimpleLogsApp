from rest_framework import serializers
from .models import AddLogs
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id', )

class AddLogsSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    sevlevel = serializers.IntegerField()
    time = serializers.DateTimeField()
    projname = serializers.CharField()
    logcont = serializers.CharField()

    class Meta:
        model = AddLogs
        fields = ('__all__')