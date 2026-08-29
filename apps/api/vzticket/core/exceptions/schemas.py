from pydantic import BaseModel


class ValidationErrorItem(BaseModel):
    field: str
    message: str


class ValidationErrorResponse(BaseModel):
    code: str
    detail: str
    errors: list[ValidationErrorItem]


class ErrorResponse(BaseModel):
    code: str
    detail: str
