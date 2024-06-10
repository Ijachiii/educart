from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call the default DRF exception handler to get the standard error response
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the error message structure
        response.data = {
            "data": None,
            "errorMessage": [{
                "code": "invalid_credentials",
                "message": response.data.get("detail", "An error occurred."),
            }],
            "error": True,
        }

    return response

def error_message(serializer):
    errors = []
        
    for err in serializer.errors:
        errors.append({
        "code": f"{err}_field",
        "message": str(serializer.errors[err][0])
    })
        
    return errors