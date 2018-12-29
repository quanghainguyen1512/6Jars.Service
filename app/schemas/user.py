from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 8
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}

def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e.message}
    except SchemaError as e:
        return {'ok': False, 'message': e.message}
    return {'ok': True, 'data': data}