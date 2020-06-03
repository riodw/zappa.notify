Notes on Testing
Create a notification and send it to the notifications endpoint. The script takes two arguments:
1. type, 0=Email, 2=SMS
2. recipient, provide either an email or phone number

Make sure that the notify virtual environment is activated in order to make use of the requests library
From this directory run either of the following commands 

	python testrunner.py 0 email@email.com
	python testrunner.py 1 5701231234

The script will atempt to make a request to create the notification, if the request succeeds the response will contain a 'public_id' string for the notification. If a 'public_id' was returned the script will then immediately call the run endpoint to send the notification. If the request succeeds it will return 'Success'


# For Deleteing

python
import requests
import json
data = {'public_ids': ['fa77dc05d3e84379b5fa19b4d5aff236']}
r = requests.delete("https://notify.medtricslab.com/api/email/delete/", json=data)
r.text


