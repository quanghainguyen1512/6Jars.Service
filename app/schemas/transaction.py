from flask_restful.fields import String, Integer, Url, Boolean, DateTime

transaction_field = {
    'type': String,
    'value': Integer,
    'note': String,
    'created_date': DateTime,
    'img_metadata': String,
    'category_id': String
}