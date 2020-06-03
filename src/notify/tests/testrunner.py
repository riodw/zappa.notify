#!/usr/bin/env python

'''
Create a notification and send it to the notifications endpoint
'''

import argparse
import requests
import datetime
import pytz
import time

BASE_URL = 'https://notify.medtricslab.com/api/'
EMAIL_URL = 'email/'
SMS_URL = 'sms/'

tz = pytz.timezone('US/Eastern')

argparser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description='Send test data to the notifications endpoint',
	epilog='''\
Example:
	python testrunner.py 0 rio@medtricslab.com
	python testrunner.py 1 16104175096

'''
)

argparser.add_argument('type', type=int, default=0, help='0=Email, 1=SMS')
argparser.add_argument('recipient', help='recipeint of the notification. Provide email address or phone number')
#argparser.add_argument('message', help='Content of the message')
NAME_SPACE = argparser.parse_args()
args = vars(NAME_SPACE)

data = {
	'recipient': args['recipient'],
	'message': 'Test message',
	'datetime': datetime.datetime.now(tz=tz) + datetime.timedelta(minutes=1)
}
# 2017-10-26 16:26:37.644379-04:00

def send(url):
	print('Sending notification...')
	try:
		r = requests.post(BASE_URL + url, data=data)
		response = r.json()
		if 'public_id' in response:
			print('Your notification public_id is:', response['public_id'])
			print()
			print(data['datetime'])
			print('Waiting 1 minute')
			
			time.sleep(60)
			print("Calling run...")
			try:
				r = requests.get(BASE_URL + 'run/')
				response = r.json()
				print(response)
			except:
				print('Failed to send request')
		else:
			print('Failed to create notification')
			print('Reason:', response)
	except:
		print('Failed to send request')

if args['type'] is 0:
	send(EMAIL_URL)
elif args['type'] is 1:
	send(SMS_URL)
elif args['type'] is 2:
	print('Push notifications are unsupported at this time')

else:
	print('Invalid type argument')