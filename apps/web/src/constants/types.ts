export type ErrorResponse = {
  code: string;
  detail: string;
}

export type FieldError = {
  field: string;
  message: string;
}

export type ValidationErrorResponse = {
  code: string;
  detail: string;
  errors: FieldError[]
}
