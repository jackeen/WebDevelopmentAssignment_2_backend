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
                    error_data = json.loads(error_content)
                except json.JSONDecodeError:
                    error_data = {"detail": error_content}

                print('error: ', response.status_code, response.content)

                def extract_messages(data):
                    messages = []
                    if isinstance(data, dict):
                        for value in data.values():
                            messages.extend(extract_messages(value))
                    elif isinstance(data, list):
                        messages.extend(data)
                    return messages

                error = extract_messages(error_data)

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
