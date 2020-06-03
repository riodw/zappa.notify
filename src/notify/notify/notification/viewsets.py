import os
import re
import random
import datetime
import boto3
import requests
from six import string_types

# Django
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import (
	authenticate,
	login,
)
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.hashers import (
	check_password,
	make_password,
)
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

# Rest
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings
from rest_framework.decorators import detail_route, list_route
from rest_framework.pagination import PageNumberPagination
from rest_framework import (
	viewsets,
	filters,
	status,
	permissions,
	mixins,
)

# APP
# Models
from .models import (
	Notification,
)
# Constants
from .constants import *
# Serializers
from .serializers import (
	NotificationSerializer,
	CreateEmailNotification,
	CreateSMSNotification,
	CreatePushNotification,
)
# App - Filters
# from .filters import (
#     NotificationFilterSet,
# )

# 
if settings.DEBUG:
	DISABLE_AWS_SNS = True
	DISABLE_AWS_SES = True
else:
	DISABLE_AWS_SNS = False
	DISABLE_AWS_SES = False


# Helper function
def canonical_phone_number(phone):
	if not isinstance(phone, string_types):
		return None
	return '+' + re.sub('[^0-9]', '', phone)


def send_email_message(notification):

	# validate addresses ## http://stackoverflow.com/questions/8022530/python-check-for-valid-email-address
	# If the email string does not pass the regex return early
	if not re.match(r"[^@]+@[^@]+\.[^@]+", notification.recipient):
		notification.runs += 1
		notification.save()
		return

	# If we're running in production send an email
	# Else print to console
	if DISABLE_AWS_SES == False and notification.sent == False:

		# http://boto3.readthedocs.io/en/latest/reference/services/ses.html#SES.Client.send_email
		try:
			# Send
			client = boto3.client('ses', region_name='us-east-1')
			response = client.send_email(
				Source= SOURCE_EMAIL,
				Destination={
					'ToAddresses': [
						notification.recipient,
					],
				},
				Message={
					'Body': {
						'Text': {
							'Charset': 'UTF-8',
							'Data': notification.message,
						},
					},
					'Subject': {
						'Charset': 'UTF-8',
						'Data': notification.subject,
					},
				},
			)

			notification.sent = True
			notification.save()
			print('Message Sent: ', notification.recipient)
			pass
		except:
			notification.runs += 1
			notification.save()
			print("Email not sent")
			return

	else:
		# THIS IS JUST FOR DEMO PURPOSES
		print('DEMO message to: ', notification.recipient, ' Subject: ', notification.subject, ' Message: ', notification.message)
		notification.sent = True
		notification.save()
	return


def send_sms_message(notification):

	# validate numbers 
	# http://stackoverflow.com/questions/6478875/regular-expression-matching-e-164-formatted-phone-numbers
	# If the phone number string does not pass the regex return early
	if not re.match(r"^\+?[1-9]\d{1,14}$", notification.recipient):
		notification.runs += 1
		notification.save()
		return

	# http://boto3.readthedocs.io/en/latest/reference/services/sns.html
	# create
	if not DISABLE_AWS_SNS:
		try:
			client = boto3.client('sns', region_name='us-east-1')
			client.publish(PhoneNumber=notification.recipient, Message=notification.message)
			notification.sent = True
			notification.save()
		except expression as identifier:
			notification.runs += 1
			notification.save()
			print("SMS not sent")
			return
	else:
		print('Sending message to:', notification.recipient, 'Message:', notification.message)
		notification.sent = True
		notification.save()
	return


def run_all_notifications():
	queryset = Notification.objects.filter(
		Q(
			datetime__lte=timezone.now(),
			runs__lt=10,
			sent=False,
			active=True
		),
	)

	numberSent = 0

	for notification in queryset.all():
		if notification.type == EMAIL:
			send_email_message(notification)
			numberSent += 1
		elif notification.type == SMS:
			send_sms_message(notification)
			numberSent += 1
		elif notification.type == PUSH:
			numberSent += 1
			pass
		else:
			pass

	return numberSent

# Notifications
#################
class NotificationViewSet(viewsets.ModelViewSet):
	queryset = Notification.objects.all()
	serializer_class = NotificationSerializer
	# filter_class = NotificationFilterSet



# Email
#################
class EmailViewSet(mixins.ListModelMixin,
					mixins.RetrieveModelMixin,
					mixins.CreateModelMixin,
					mixins.DestroyModelMixin,
					viewsets.GenericViewSet):
	"""
	Endpoints for managing notifications.

	email/create:
	Create a new notification instance of type EMAIL.

	sms/create:
	Create a new notification instance of type SMS.

	run:
	Sends all availible notifications.

	destroy:
	Destroy a notification instance

	list:
	Return a list of all the existing notifications.

	get:
	Return the given notification.
	"""

	serializer_class = NotificationSerializer
	permission_classes = (AllowAny,)
	http_method_names = ['get','post','delete']

	def get_queryset(self):
		return Notification.objects.filter(
			Q(type=EMAIL),
		)

	# Create Email
	def create(self, request):
		serializer = CreateEmailNotification(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)

		run_all_notifications()

		return Response({'public_id': serializer.data['public_id']}, status=status.HTTP_201_CREATED, headers=headers)

	# Delete Email
	@list_route(methods=['delete'])
	def delete(self, request):
		if request.data:

			if request.data['public_ids']:

				public_ids = request.data['public_ids']

				if isinstance(public_ids, list):

					badIdArray = []

					for public_id in public_ids:
					
						if isinstance(public_id, str) and len(public_id) is 32 and '-' not in public_id:
							try:
								notif = Notification.objects.get(public_id=public_id, type=EMAIL)
								notif.active = False
								notif.save()
							
							except:
								badIdArray.append(public_id)
						else:
							badIdArray.append(public_id)

					if len(badIdArray):
						return Response(
							{'FAIL: Items not found': badIdArray},
							status=status.HTTP_400_BAD_REQUEST
						)
					else:
						return Response(
							'SUCCESS: All Deactivated',
							status=status.HTTP_200_OK
						)
				
				return Response(
					{'FAIL: Not an Array': public_id},
					status=status.HTTP_400_BAD_REQUEST
				)
			
			return Response(
				'FAIL: No public_id sent',
				status=status.HTTP_400_BAD_REQUEST
			)
		
		return Response(
			'FAIL: No Data',
			status=status.HTTP_400_BAD_REQUEST
		)

	# List All Emails
	def list(self, request):
		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	# List One Email
	def retrieve(self, request, pk=None):
		if request.data:

			if request.data['public_id']:
				public_id = request.data['public_id']

				if len(public_id) is 32:
					try:
						notif = Notification.objects.get(
							public_id=public_id,
							type=EMAIL
						)
						serializer = NotificationSerializer(notif)
						return Response(
							serializer.data,
							status=status.HTTP_200_OK
						)
					
					except:
						return Response(
							{'FAIL: Item not found': public_id},
							status=status.HTTP_400_BAD_REQUEST
						)

				return Response(
					{'FAIL: Not Valid public_id': public_id},
					status=status.HTTP_400_BAD_REQUEST
				)
			
			return Response(
				'FAIL: No public_id sent',
				status=status.HTTP_400_BAD_REQUEST
			)
		
		return Response(
			'FAIL: No Data',
			status=status.HTTP_400_BAD_REQUEST
		)


# SMS
#################
class SMSViewSet(mixins.ListModelMixin,
				 	mixins.RetrieveModelMixin,
				 	mixins.CreateModelMixin,
				 	mixins.DestroyModelMixin,
				 	viewsets.GenericViewSet):

	serializer_class = NotificationSerializer
	permission_classes = (AllowAny,)
	http_method_names = ['get','post','delete']

	def get_queryset(self):
		return Notification.objects.filter(
			Q(type=SMS),
		)

	# Create SMS
	def create(self, request):
		serializer = CreateSMSNotification(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)

		# Runs
		run_all_notifications()
		
		return Response(
			{'public_id': serializer.data['public_id']},
			status=status.HTTP_201_CREATED,
			headers=headers
		)

	# Delete SMS
	def delete(self, request):
		if request.data:

			if request.data['public_ids']:

				public_ids = request.data['public_ids']

				if isinstance(public_ids, list):

					badIdArray = []

					for public_id in public_ids:
					
						if isinstance(public_id, str) and len(public_id) is 32 and '-' not in public_id:
							try:
								notif = Notification.objects.get(public_id = public_id, type = SMS)
								notif.active = False
								notif.save()
							
							except:
								badIdArray.append(public_id)
						else:
							badIdArray.append(public_id)

					if len(badIdArray):
						return Response({'FAIL: Items not found': badIdArray},status=status.HTTP_400_BAD_REQUEST)
					else:
						return Response('SUCCESS: All Deactivated', status=status.HTTP_200_OK)
				
				return Response({'FAIL: Not an Array': public_id},status=status.HTTP_400_BAD_REQUEST)
			
			return Response('FAIL: No public_id sent',status=status.HTTP_400_BAD_REQUEST)
		
		return Response('FAIL: No Data',status=status.HTTP_400_BAD_REQUEST)

	# List All SMS
	def list(self, request):
		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	# List One SMS
	def retrieve(self, request, pk=None):
		if request.data:

			if request.data['public_id']:
				public_id = request.data['public_id']

				if len(public_id) is 32:
					try:
						notif = Notification.objects.get(public_id = public_id, type = SMS)
						serializer = NotificationSerializer(notif)
						return Response(serializer.data, 						status=status.HTTP_200_OK)
					
					except:
						return Response({'FAIL: Item not found': public_id},status=status.HTTP_400_BAD_REQUEST)

				return Response({'FAIL: Not Valid public_id': public_id},status=status.HTTP_400_BAD_REQUEST)
			
			return Response('FAIL: No public_id sent',status=status.HTTP_400_BAD_REQUEST)
		
		return Response('FAIL: No Data',status=status.HTTP_400_BAD_REQUEST)


# PUSH
#################
class PushViewSet(mixins.ListModelMixin,
					mixins.RetrieveModelMixin,
					mixins.DestroyModelMixin,
					viewsets.GenericViewSet):
	
	serializer_class = NotificationSerializer
	permission_classes = (AllowAny,)
	http_method_names = ['get','post','delete']

	def get_queryset(self):
		return Notification.objects.filter(
			Q(type=PUSH),
		)

	# Delete Notification by ID
	def delete(self, request):
		if request.data:

			if request.data['public_id']:
				public_id = request.data['public_id']

				if len(public_id) is 32:
					try:
						notif = Notification.objects.get(public_id = public_id)
						notif.active = False
						notif.save()
						return Response(
							{'public_id': notif.public_id},
							status=status.HTTP_200_OK,
						)
					
					except:
						return Response(
							{'FAIL: Item not found': public_id},
							status=status.HTTP_400_BAD_REQUEST,
						)

				return Response(
					{'FAIL: Not Valid public_id': public_id},
					status=status.HTTP_400_BAD_REQUEST,
				)
			
			return Response(
				'FAIL: No public_id sent',
				status=status.HTTP_400_BAD_REQUEST,
			)
		
		return Response(
			'FAIL: No Data',
			status=status.HTTP_400_BAD_REQUEST,
		)

	# List All Notifications
	def list(self, request):
		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	# List One Notification
	def retrieve(self, request, pk=None):
		queryset = Notification.objects.all()
		notification = get_object_or_404(queryset, pk=pk)
		serializer = NotificationSerializer(user)
		return Response(serializer.data)


# RUN
#################
class RunViewSet(mixins.ListModelMixin,
					viewsets.GenericViewSet):
	
	serializer_class = NotificationSerializer
	permission_classes = (AllowAny,)
	http_method_names = ['get','post','delete']
	
	# RUN SEND NOTIFICATIONS
	def list(self, request):

		return Response(
			'Success: Sent ' + str(run_all_notifications()) + ' messages.'
		)