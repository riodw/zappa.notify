import os
import sys
from django.conf import settings

# Notification type constants
EMAIL = 0
SMS = 1
PUSH = 2

# Sourc Email
SOURCE_EMAIL = 'rio@medtricslab.com'
if settings.DEBUG == False:
    # Email
    try:
        SOURCE_EMAIL = os.environ['SOURCE_EMAIL']
    except KeyError as e:
        print("*********************************************")
        print("SOURCE_EMAIL environment variable is required")
        print("*********************************************")
        sys.exit()