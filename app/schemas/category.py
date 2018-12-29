from flask_restful.fields import String, Url

category_fields = {
    'name': String,
    'description': String,
    'parent_cate': String,
    'uri': Url('categories')
}