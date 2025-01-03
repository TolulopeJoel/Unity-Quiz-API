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
        response_data = response.data
        if response.status_code >= 400:
            response_data = response_data or {}
            response_data.setdefault('status', response.status_code)

            error_info = self._extract_error_info(response_data)
            response_data['message'] = error_info['message']
            if error_info['field']:
                response_data['field'] = error_info['field']

            self._remove_error_fields(response_data)

        return response_data

    def _remove_error_fields(self, response_data):
        """
        Remove keys that contain error messages.
        """
        keys_to_remove = []

        for key, value in response_data.items():
            if key not in ['message', 'field', 'status']:
                if isinstance(value, list) and value:
                    keys_to_remove.append(key)
                elif isinstance(value, dict) and value:
                    self._remove_error_fields(value)

        for key in keys_to_remove:
            del response_data[key]

    def _extract_error_info(self, response_data):
        """
        Extract error message and field information from the response data.
        Returns a dict with 'message' and 'field' keys.
        """
        if message := response_data.get('message'):
            return {'message': message, 'field': None}

        if detail := response_data.get('detail'):
            return {'message': str(detail), 'field': None}

        if errors := response_data.get('non_field_errors'):
            return {'message': errors[0], 'field': None}

        for key, value in response_data.items():
            # If value is a non-empty list, return first item as error message
            if isinstance(value, list) and value:
                return {'message': value[0], 'field': key}

            # If value is a dictionary, recursively extract nested error info
            elif isinstance(value, dict):
                nested_error = self._extract_error_info(value)
                if nested_error['field']:
                    return {
                        'message': nested_error['message'],
                        'field': f"{key}.{nested_error['field']}" 
                    }
                return {
                    'message': f"{nested_error['message']}",
                    'field': key
                }

        return {'message': _('An error occurred'), 'field': None}
