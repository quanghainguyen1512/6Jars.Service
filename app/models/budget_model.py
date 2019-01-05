from app import mongo

default_budget = {
    'user': '',
    'total': 0,
    'nec': {
        'fullname': 'Necessities',
        'shortname': 'NEC',
        'proportion': 0.5,
        'subtotal': 0
    },
    'ply': {
        'fullname': 'Play',
        'shortname': 'PLY',
        'proportion': 0.1,
        'subtotal': 0
    },
    'giv': {
        'fullname': 'Give',
        'shortname': 'GIV',
        'proportion': 0.1,
        'subtotal': 0
    },
    'lts': {
        'fullname': 'Long-term saving',
        'shortname': 'LTS',
        'proportion': 0.1,
        'subtotal': 0
    },
    'edu': {
        'fullname': 'Education',
        'shortname': 'EDU',
        'proportion': 0.1,
        'subtotal': 0
    },
    'ffr': {
        'fullname': 'Financial Freedom',
        'shortname': 'FIN',
        'proportion': 0.1,
        'subtotal': 0
    }
}

def init_budget(user):
    default_budget['user'] = user
    res = mongo.db.budgets.insert_one(default_budget)
    return res.acknowledged

def update_percent(user, newjars):
    newValue = { '$set': {
        'nec.proportion': newjars['nec']['proportion'],
        'ply.proportion': newjars['ply']['proportion'],
        'giv.proportion': newjars['giv']['proportion'],
        'lts.proportion': newjars['lts']['proportion'],
        'edu.proportion': newjars['edu']['proportion'],
        'ffr.proportion': newjars['ffr']['proportion'],
    }}
    res = mongo.db.budgets.update_one({ 'user': user }, newValue)
    return res.acknowledged

def update_for_expense(transaction):
    trans_val = transaction['value']
    res = mongo.db.budgets.update_one({ '_id': transaction['budget_id'] },
    {
        '$inc': {
            'total': -trans_val,
            transaction['jar']: -trans_val
        }
    })
    return res.acknowledged

def update_budget_for_transaction(transaction):
    trans_val = transaction['value']
    if transaction['type'] == 'expense':
        trans_val = -trans_val
    elif transaction['type'] == 'expense' and 'jar' not in transaction:
        cur_bud = mongo.db.budgets.find_one({ '_id': transaction['budget_id'] }, { 'user': 0, 'total': 0 })
        res = mongo.db.budgets.update_one({ '_id': transaction['budget_id'] }, 
        {
            '$inc': { 
                'total': trans_val,
                'nec.subtotal': trans_val * cur_bud['nec']['proportion'],
                'ply.subtotal': trans_val * cur_bud['ply']['proportion'],
                'giv.subtotal': trans_val * cur_bud['giv']['proportion'],
                'edu.subtotal': trans_val * cur_bud['edu']['proportion'],
                'lts.subtotal': trans_val * cur_bud['lts']['proportion'],
                'ffr.subtotal': trans_val * cur_bud['ffr']['proportion'],
            }
        })
        return res.acknowledged

    res = mongo.db.budgets.update_one({ '_id': transaction['budget_id'] },
    {
        '$inc': {
            'total': trans_val,
            transaction['jar']: trans_val
        }
    })
    return res.acknowledged
    
def update_for_income(transaction):
    cur_bud = mongo.db.budgets.find_one({ '_id': transaction['budget_id'] }, { 'user': 0, 'total': 0 })
    
    trans_val = transaction['value']

    res = mongo.db.budgets.update_one({ '_id': transaction['budget_id'] }, 
    {
        '$inc': { 
            'total': trans_val,
            'nec.subtotal': trans_val * cur_bud['nec']['proportion'],
            'ply.subtotal': trans_val * cur_bud['ply']['proportion'],
            'giv.subtotal': trans_val * cur_bud['giv']['proportion'],
            'edu.subtotal': trans_val * cur_bud['edu']['proportion'],
            'lts.subtotal': trans_val * cur_bud['lts']['proportion'],
            'ffr.subtotal': trans_val * cur_bud['ffr']['proportion'],
        }
    })
    return res.acknowledged

def get_budget(user):
    return mongo.db.budgets.find_one({ 'user': user })

# def check_can_decrease(user, jar, decrease_val):
#     data = mongo.budgets.find_one({ 'user': user })
#     if data[jar]['subtotal'] - decrease_val < 0:
#         return False
#     if data['total'] - decrease_val < 0:
#         return False
#     return True
