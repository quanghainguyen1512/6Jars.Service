from app import mongo

def get_category_by_name(name):
    return mongo.db.categories.find_one({'name': name})

def get_all_categories():
    return mongo.db.categories.find({}, { '_id': 0 })

def add_new_category(data):
    res = mongo.db.categories.insert_one(data)
    return res['acknowledged']