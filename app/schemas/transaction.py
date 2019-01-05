transaction_schema = {
    'type': 'object',
    'properties': {
        'category_id': {
            'type': 'objectId'
        },
        'jar': {
            'type': 'string',
            'maxLength': 3
        },
        'budget_id': {
            'type': 'objectId'
        },
        'user': {
            'type': 'string'
        },
        'type': {
            'type': 'string',
            'enum': ['expense', 'income', 'dept', 'loan']
        },
        'value': {
            'type': 'number'
        }
    },
    'required': ['category_id', 'budget_id', 'user', 'type', 'value'],
    'additionalProperties': True
}
