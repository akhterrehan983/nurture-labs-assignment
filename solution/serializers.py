
from rest_framework import serializers
from . models import advisor, user
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('id', 'name', 'email', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

class addAdvisorSearializer(serializers.ModelSerializer):
    class Meta:
        model = advisor
        fields = ["id","name","photo"]

class dateTimeSerializer(serializers.Serializer): # define a serializer with a datetime field
    dateTime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")