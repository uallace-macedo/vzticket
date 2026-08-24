from pydantic import BaseModel


class ValidationErrorItem(BaseModel):
    field: str
    message: str


class ValidationErrorResponse(BaseModel):
    code: str = 'VALIDATION_ERROR'
    detail: str = 'Dados de requisição inválidos'
    errors: list[ValidationErrorItem]


class ErrorResponse(BaseModel):
    code: str
    detail: str
