from .user import user_schema
from .transaction import transaction_schema
from .budget import budget_schema
from jsonschema import ValidationError, SchemaError, validate

def validate_data(data, schema):
    try:
        validate(data, schema)
    except ValidationError as e:
        return {'ok': False, 'message': e.message}
    except SchemaError as e:
        return {'ok': False, 'message': e.message}
    return {'ok': True, 'data': data}