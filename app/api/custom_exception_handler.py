from django.http import Http404
from rest_framework.views import exception_handler
from rest_framework.exceptions import NotFound

def custom_exception_handler(exc, context):
    
    # Call REST framework's default exception handler
    response = exception_handler(exc, context)
    # Add the HTTP status code to the response
    if response is not None:
        response.data['status_code'] = response.status_code
    
    return response