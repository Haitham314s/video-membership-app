from fastapi import HTTPException


class LoginRequiredException(HTTPException):
    pass


class UserHasAccountException(Exception):
    """User already has an account."""


class InvalidEmailException(Exception):
    """Invalid user email"""


class InvalidUserIDException(HTTPException):
    pass
