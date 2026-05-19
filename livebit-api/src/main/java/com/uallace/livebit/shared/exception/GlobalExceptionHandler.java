package com.uallace.livebit.shared.exception;

import com.fasterxml.jackson.databind.exc.InvalidFormatException;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ExceptionResponse<Map<String, String>>> handleValidationException(MethodArgumentNotValidException ex, HttpServletRequest req) {
        Map<String, String> errors = new HashMap<>();

        ex.getBindingResult().getAllErrors().forEach(error -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });

        ExceptionResponse<Map<String, String>> response = new ExceptionResponse<>(
                LocalDateTime.now(),
                "Validation error",
                req.getRequestURI(),
                errors
        );

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ExceptionResponse<Map<String, String>>> handleHttpMessageNotReadableException(HttpMessageNotReadableException ex, HttpServletRequest req) {
        Map<String, String> errors = new HashMap<>();

        if(ex.getCause() instanceof InvalidFormatException formatException) {
            if (formatException.getTargetType().isEnum()) {
                String fieldName = formatException.getPath().getFirst().getFieldName();
                String acceptedValues = Arrays.toString(formatException.getTargetType().getEnumConstants());
                String message = String.format("Invalid value for field '%s'. Accepted values are: %s", fieldName, acceptedValues);

                errors.put(fieldName, message);
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                        new ExceptionResponse<>(
                                LocalDateTime.now(),
                                "Invalid enum value",
                                req.getRequestURI(),
                                errors
                        )
                );
            }
        }

        errors.put("error", "Malformed JSON request body");
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                new ExceptionResponse<>(
                        LocalDateTime.now(),
                        "Invalid request",
                        req.getRequestURI(),
                        errors
                )
        );
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ExceptionResponse<Void>> handleGlobalExceptions(Exception ex, HttpServletRequest req) {
        ExceptionResponse<Void> error = new ExceptionResponse<>(
                LocalDateTime.now(),
                ex.getMessage(),
                req.getRequestURI()
        );

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
