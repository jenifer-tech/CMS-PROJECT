from rest_framework.exceptions import APIException

class CommentsNotFoundException(APIException):
    status_code=404
    default_detail='Comments Not Found'
    code='Comments_Not_Found'