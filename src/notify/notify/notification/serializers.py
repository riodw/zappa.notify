import boto3
import datetime
import re
import random
import logging
import json
from six import string_types

# Django
from django.db.models import Q
from django.conf import settings
from django.utils import timezone

# Rest
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response as rf_Response

# App
from .models import (
    Notification,
)
from .constants import *


# 
if settings.DEBUG:
    DISABLE_AWS_SNS = True
    DISABLE_SENDGRID = True
else:
    DISABLE_AWS_SNS = False
    DISABLE_SENDGRID = False


# Helper function
def canonical_phone_number(phone):
    if not isinstance(phone, string_types):
        return None
    return '+' + re.sub('[^0-9]', '', phone)



# Serializers define the API representation.
# class NotificationSerializer(serializers.Serializer):
# 	# id = serializers.IntegerField(read_only=True)
# 	public_id = serializers.CharField(read_only=True)
# 	created_date = serializers.DateTimeField(read_only=True)
# 	message = serializers.CharField(read_only=True)
# 	subject = serializers.CharField(read_only=True)
# 	datetime = serializers.DateTimeField(read_only=True)
# 	recipient = serializers.EmailField(read_only=True)
# 	sender = serializers.EmailField(read_only=True)
# 	source = serializers.CharField(read_only=True)
# 	type = serializers.IntegerField(read_only=True)
# 	runs = serializers.IntegerField(read_only=True)
# 	sent = serializers.BooleanField(read_only=True)
# 	active = serializers.BooleanField(read_only=True)
    


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'








class CreateEmailNotification(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	public_id = serializers.CharField(read_only=True)
	message = serializers.CharField()
	subject = serializers.CharField(default='Notification')
	# recipient = serializers.CharField() # OLD
	recipient = serializers.EmailField()
	sender = serializers.EmailField(default=SOURCE_EMAIL)
	source = serializers.CharField(default='Notify') # What app the notification is being created from

	def create(self, validated_data):

		# OLD
		# if not re.match(r"[^@]+@[^@]+\.[^@]+", validated_data['recipient']):
		# 	raise serializers.ValidationError('Valid email not provided')

		validated_data['type'] = EMAIL
        
		notification = Notification.objects.create(**validated_data)
		return notification



class CreateSMSNotification(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	public_id = serializers.CharField(read_only=True)
	message = serializers.CharField()
	datetime = serializers.DateTimeField()
	recipient = serializers.CharField()

	def create(self, validated_data):

		if not re.match(r"^\+?[1-9]\d{1,14}$", validated_data['recipient']):
			raise serializers.ValidationError('Valid phone number not provided')

		if len(validated_data['recipient']) <= 10:
			raise serializers.ValidationError('Phone number not greater than 10 digits')

		validated_data['type'] = SMS
		validated_data['recipient'] = canonical_phone_number(validated_data['recipient'])

		notification = Notification.objects.create(**validated_data)
		return notification



class CreatePushNotification(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	public_id = serializers.CharField(read_only=True)
	message = serializers.CharField()
	datetime = serializers.DateTimeField()
	recipient = serializers.CharField()

	def create(self, validated_data):

		validated_data['type'] = PUSH

		notification = Notification.objects.create(**validated_data)
		return notification