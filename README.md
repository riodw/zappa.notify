# My project's README

Setup

1. Clone project

2. Turn top level notify directory in python3 virtual envirnemnt
$ python3 -m venv notify

3. Install requirements
$ pip3 install -r requirements.txt

3. Run migrations
$ cd notify
$ python manage.py migrate


Update Zappa settings
This applications runs django on a serverless AWS Lambda enviroment using Miserlou's Zappa project.
Update the notify/zappa_settings.json file with your own configuration


Required environment variables:
DEV or PROD
Variable the specifies how the application will run
DEV: runs in DJANO DEBUG=True and will disable all AWS functions and print message sending info to console
PROD: runs in DJANGO DEBUG=FALSE and will enable all AWS functions

APP_NAME
A name specified for the application and will be used in the subject line of email messages

SOURCE_EMAIL
An email used by AWS SES that is verified that you can send from.
Chack and make sure you have a verified email to send messages to or
have requested a rate increase taking your SES out of sandbox mode.


Database environment variables
Postgres database required

RDS_DB_NAME

RDS_HOSTNAME

RDS_USERNAME

RDS_PASSWORD

RDS_PORT



Testing notifications

# Start virtual environment
import requests
import datetime
import pytz
tz = pytz.timezone('US/Eastern')
# Create a notification for 5 minutes from now
dt = datetime.datetime.now(tz=tz) + datetime.timedelta(minutes=10)
data = data = {"recipient":"test@test.com","message":"Test","datetime":dt}
r = requests.post("http://127.0.0.1:8000/api/notifications/create_email/", data=data)
r = requests.get("http://127.0.0.1:8000/api/notifications/go/")
Should send no notification
# Wait 5 mins
r = requests.get("http://127.0.0.1:8000/api/notifications/go/")
# Should send one notification

