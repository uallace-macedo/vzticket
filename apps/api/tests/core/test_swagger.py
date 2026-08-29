from vzticket.core.exceptions.base import AppError
from vzticket.core.exceptions.schemas import ErrorResponse
from vzticket.core.exceptions.swagger import create_error_response


class CustomTestError(AppError):
    status_code = 400
    code = 'CUSTOM_TEST_ERROR'
    message = 'Mensagem de erro de teste customizada'


def test_create_error_response_structure():
    description = 'Descrição do erro para o Swagger'
    response_schema = create_error_response(CustomTestError, description)

    assert response_schema['model'] == ErrorResponse
    assert response_schema['description'] == description

    example = response_schema['content']['application/json']['example']
    assert example['code'] == 'CUSTOM_TEST_ERROR'
    assert example['detail'] == 'Mensagem de erro de teste customizada'
