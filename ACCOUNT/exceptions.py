from rest_framework.exceptions import APIException

class AccountNotFoundException(APIException):
    status_code=404
    default_detail='Account Not Found'
    code='Account_Not_Found'