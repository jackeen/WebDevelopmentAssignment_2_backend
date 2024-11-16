import json

from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response


class JSONResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        success = False
        error = None
        data = None
        if isinstance(response, Response):
            if response.status_code >= 400:
                # error = response.data.get("detail", "An error occurred")
                try:
                    error_content = response.content.decode('utf-8')
                    error = json.loads(error_content)
                except json.JSONDecodeError:
                    error = {"detail": error_content}
                print('error: ', response.status_code, response.content)
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
