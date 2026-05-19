package com.uallace.livebit.auction.exceptions;

import com.uallace.livebit.shared.exception.ExceptionResponse;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.time.LocalDateTime;

@ControllerAdvice
public class AuctionExceptionsHandler {
    @ExceptionHandler(InvalidEndsAtException.class)
    public ResponseEntity<ExceptionResponse<Void>> handleInvalidEndsAtException(InvalidEndsAtException ex, HttpServletRequest req) {
        ExceptionResponse<Void> error = new ExceptionResponse<>(
                LocalDateTime.now(),
                ex.getMessage(),
                req.getRequestURI()
        );

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }
}
