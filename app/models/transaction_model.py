from app import mongo

transaction = {
    'value': 0,
    'category_id': 'adasd',
    'jar': 'nec',
    'budget_id': 'zxczxc',
    'user': 'asdasd',
    'type': 'expense',
}

def add_transaction(transaction):
    assert transaction['user']
    res = mongo.db.transaction.insert_one(transaction)
    transaction['value']
    return res.acknowledged, res.inserted_id

def update_transaction(id, transaction):
    res = mongo.db.transactions.replace_one({ '_id': id }, transaction)
    return res.acknowledged

def delete_transaction(id):
    mongo.db.transactions.delete_one({ '_id': id })

def get_transactions(start_date, end_date, user, jar=None, type=None):
    _filter = {
        'date': { '$lte': end_date, '$gte': start_date },
        'user': user
    }
    if jar:
        _filter['jar'] = jar
    if type:
        _filter['type'] = type
    
    projection = {
        'category_id': 1,
        'value': 1,
        'type': 1
    }
    res = mongo.db.transactions.find(_filter, projection)
    return res

def get_transaction_by_id(user, tran_id):
    res = mongo.db.transactions.find_one({ '_id': tran_id, 'user': user })
    return res