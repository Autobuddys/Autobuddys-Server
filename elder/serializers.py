from rest_framework import serializers
from elder import models

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id','name','email','password','phone','is_medical')
        extra_kwargs = {
            'password':{
                'write_only' : True,
                'style' : {'input_type':'password'}
            }
        }
    
    def create(self,validated_data):
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            is_medical=validated_data['is_medical']
        )
        return user
    
    def validate_phone(self,value):
        if len(value)<10:
            raise serializers.ValidationError('Invalid phone number!')
        return value


class MedicalStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalStaff
        fields = '__all__'
    
    def validate_pincode(self,value):
        if value>855117 or value<110001:
            raise serializers.ValidationError('Invalid pin code!')
        return value

class PatientRelativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PatientRelative
        fields= '__all__'

    def validate_pincode(self,value):
        value = int(value)
        if value>855117 or value<110001:
            raise serializers.ValidationError('Invalid pin code!')
        return value
    
    def validate_pphone(self,value):
        if len(value)<10:
            raise serializers.ValidationError('Invalid phone number!')
        return value
    
    def validate_dphone(self,value):
        if len(value)<10:
            raise serializers.ValidationError('Invalid phone number!')
        return value

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields= '__all__'


class VitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vital
        fields = '__all__'
    def create(self, validated_data):
      vital1 = models.Vital.objects.create(**validated_data)
      return vital1


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageStore
        fields = '__all__'

class PatientImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PatientImage
        fields = '__all__'