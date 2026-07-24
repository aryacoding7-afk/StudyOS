class AppException(Exception):
    """Base class for all application exceptions."""

    status_code = 500
    detail = "An unexpected error occurred."

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)


class BadRequestException(AppException):
    status_code = 400


class UnauthorizedException(AppException):
    status_code = 401


class ForbiddenException(AppException):
    status_code = 403


class NotFoundException(AppException):
    status_code = 404


class ConflictException(AppException):
    status_code = 409


class EmailAlreadyExistsException(ConflictException):
    detail = "Email already registered."


class UsernameAlreadyExistsException(ConflictException):
    detail = "Username already taken."


class InvalidCredentialsException(UnauthorizedException):
    detail = "Invalid email or password."


class FileTypeNotSupportedException(BadRequestException):
    detail = "Only PDF files are allowed."


class DocumentNotFoundException(NotFoundException):
    detail = "Document not found."

class LLMGenerationException(AppException):
    detail = "Failed to generate AI response."