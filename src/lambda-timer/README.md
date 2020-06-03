Lambda Timer

Required Environment Variables
ENDPOINT = Full url endpoint to call


The trigger to this function is a CloudWatch Rule, "1-Minute-Timer', that fires every minute. The Lambda function will call a url to a rest API endpoint. The endpoint is supplied as an environment variable.

In order for the function to run the python requests library is required. In order to provide the library to the function you must first create a python virtual environment and then use pip to install requests. Copy the following items out of the the vitual environemnt:
[Environment name]/lib/python3.6/site-packages/
certifi, chardet, idna, requests, urllib3

Uploading the lambda function
Compress all items in this directory
On the AWS console under your lambda functions select the notifications-timer function
Under the configuration tab, Code entry type, select Upload a .zip file
