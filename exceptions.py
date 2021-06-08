from rest_framework.exceptions import APIException

class BlogNotFoundException(APIException):
    status_code=404
    default_detail='BlogPost Not Found'
    code='BlogPost_Not_Found'