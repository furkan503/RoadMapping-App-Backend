from rest_framework import serializers
from map.models import Datayol, Databolge
from django.contrib.auth.models import User
from django.core.serializers import serialize
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class DatayolSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Datayol
        geo_field = 'koordinat'
        fields = '__all__'

class DatabolgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Databolge
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields='__all__'
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User(username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



