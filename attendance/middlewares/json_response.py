import json

from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response


class JSONResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        success = False
        error = []
        data = None
        if isinstance(response, Response):
            if response.status_code >= 400:
                try:
                    error_content = response.content.decode('utf-8')
                    error = json.loads(error_content)
                except json.JSONDecodeError:
                    error = {"detail": error_content}

                print('error: ', response.status_code, response.content)

                if isinstance(error, dict):
                    flat_errors = []
                    for field, messages in error.items():
                        if isinstance(messages, list):
                            flat_errors.extend([f"{message} for {field}" for message in messages])
                        else:
                            flat_errors.append(f"{messages} for {field}")
                    error = flat_errors

            else:
                success = True
                data = response.data

            response["Content-Type"] = "application/json"
            response.content = json.dumps({
                "success": success,
                "error": error,
                "data": data
            })
        return response
