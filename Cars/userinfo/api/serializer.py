from rest_framework import serializers
from django.contrib.auth.models import User

class RegestraSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data.get('password') != data.get('password_confirmation'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

