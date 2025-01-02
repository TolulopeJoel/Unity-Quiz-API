import contextlib
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response


class ErrorAPIResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Skip processing for documentation paths
        if 'docs' in request.path:
            return response

        if isinstance(response, Response):
            with contextlib.suppress(Exception):
                response_data = self.render_response(response)
                response.data = response_data
                response.content = json.dumps(
                    response_data, cls=DjangoJSONEncoder
                )

        return response

    def render_response(self, response):
        """
        Format the API response and remove field names with error messages.
        """
        response_data = response.data or {}
        response_data.setdefault('status', response.status_code)

        if response.status_code >= 400:
            response_data['message'] = self._extract_error_message(response_data)

            self._remove_error_fields(response_data)

        return response_data

    def _remove_error_fields(self, response_data):
        """
        Remove keys that contain error messages.
        """
        keys_to_remove = []

        for key, value in response_data.items():
            if key != 'message':
                if isinstance(value, list) and value:
                    keys_to_remove.append(key)
                elif isinstance(value, dict) and value:
                    self._remove_error_fields(value)

        for key in keys_to_remove:
            del response_data[key]

    def _extract_error_message(self, response_data):
        """
        Extract a meaningful error message from the response data.
        """
        if message := response_data.get('message'):
            return message

        if detail := response_data.get('detail'):
            return str(detail)

        if errors := response_data.get('non_field_errors'):
            return errors[0]

        for key, value in response_data.items():
            if isinstance(value, list) and value:
                return value[0]
            elif isinstance(value, dict):
                new_value = self._extract_error_message(value)
                return f"{key}: {new_value}"

        return _('An error occurred')
