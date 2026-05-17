package org.uallace.livebit.shared;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.ConstraintViolationException;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.core.UriInfo;
import java.time.LocalDateTime;
import java.util.Map;
import java.util.stream.Collectors;
import org.jboss.resteasy.reactive.server.ServerExceptionMapper;

public class GlobalExceptionHandler {

    @ServerExceptionMapper
    public Response handleValidationException(ConstraintViolationException ex, UriInfo uriInfo) {
        Map<String, String> errors = ex
            .getConstraintViolations()
            .stream()
            .collect(
                Collectors.toMap(violation -> {
                    String path = violation.getPropertyPath().toString();
                    return path.substring(path.lastIndexOf(".") + 1);
                }, ConstraintViolation::getMessage)
            );

        ErrorResponse<Map<String, String>> err = new ErrorResponse<>(
            LocalDateTime.now(),
            "Validation error",
            uriInfo.getPath(),
            errors
        );

        return Response.status(Response.Status.BAD_REQUEST.getStatusCode())
            .entity(err)
            .build();
    }
}
