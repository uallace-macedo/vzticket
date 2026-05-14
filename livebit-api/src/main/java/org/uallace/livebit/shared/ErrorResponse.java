package org.uallace.livebit.shared;

import java.time.LocalDateTime;

public record ErrorResponse<T>(
        LocalDateTime timestamp,
        String message,
        String uri,
        T details
){}
