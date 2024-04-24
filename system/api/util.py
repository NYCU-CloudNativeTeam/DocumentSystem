from functools import wraps

from flask import jsonify, request
from marshmallow import Schema, fields, ValidationError


def validate_json(schema):
    """Decorator for validating JSON data against a given schema.

    Args:
        schema (Schema): The schema object for validation.

    Returns:
        Any: The wrapped function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # parse json content
                json_data = request.get_json()
                # using marshmallow to do validtion
                validated_data = schema().load(json_data)
                return func(validated_data, *args, **kwargs)
            except ValidationError as e:
                return jsonify({'error': str(e)}), 422
        return wrapper
    return decorator