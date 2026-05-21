from fastapi import HTTPException


class AuthenticationException(HTTPException):
    pass

class BadRequestException(HTTPException):
    pass

