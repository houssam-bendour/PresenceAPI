from rest_framework import serializers
# from rest_framework.response import Response

from .models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','rfid', 'CNE','email','first_name','last_name','username' ,'password', 'user_type','is_superuser','is_staff']
        
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                if attr == 'password':
                    instance.set_password(value)
                else:
                    setattr(instance, attr, value)
            instance.save()
            return instance
    

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"


class InscrireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscrire
        fields = "__all__"

class PresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = "__all__"

class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = "__all__"
        
        
