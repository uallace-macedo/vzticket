package com.uallace.livebit.auth.exceptions;

import com.uallace.livebit.shared.exception.ExceptionResponse;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.time.LocalDateTime;

@ControllerAdvice
public class AuthExceptionsHandler {
    @ExceptionHandler(InvalidCredentialsException.class)
    public ResponseEntity<ExceptionResponse<Void>> handleInvalidCredentialsException(InvalidCredentialsException ex, HttpServletRequest req) {
        ExceptionResponse<Void> error = new ExceptionResponse<>(
                LocalDateTime.now(),
                ex.getMessage(),
                req.getRequestURI()
        );

        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
    }

}
