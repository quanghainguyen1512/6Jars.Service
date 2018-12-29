from app import mongo

def add(jti):
    return mongo.db.revoked_tokens.insert_one({ 'jti': jti })

def check_token_is_used(jti):
    return mongo.db.revoked_tokens.find_one({ 'jti': jti })