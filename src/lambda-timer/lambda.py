import requests
import os

ENDPOINT = os.environ['ENDPOINT']

"""
Lambda functions typically call a specific method e.g. lambda.handler

This method is passed two positional arguments by AWS. It is therefore
required to have the two arguments in the function even if nothing is done
with them in the actual function.
"""

def handler(self, event):
    requests.get(ENDPOINT)
    return