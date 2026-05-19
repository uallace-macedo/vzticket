package com.uallace.livebit.shared.exception;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.time.LocalDateTime;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record ExceptionResponse<T>(
        LocalDateTime timestamp,
        String message,
        String uri,
        T details
) {
    public ExceptionResponse(LocalDateTime timestamp, String message, String uri) {
        this(timestamp, message, uri, null);
    }
}
