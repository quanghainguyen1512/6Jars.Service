from app import mongo

def find_user_by_email(email):
    if email:
        return mongo.db.users.find_one({ 'email': email }, { '_id': 0 })
    else:
        return None

def add_new_user(data):
    return mongo.db.users.insert(data)

def delete_user(email):
    if not email or not mongo.db.users.find_one({ 'email': email }, { '_id': 0 }):
        return False
    res = mongo.db.users.delete_one({ 'email': email })
    return int(res['deleted_count']) > 0