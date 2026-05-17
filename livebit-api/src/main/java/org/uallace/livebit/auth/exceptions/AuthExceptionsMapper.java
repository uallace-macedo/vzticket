package org.uallace.livebit.auth.exceptions;

import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.core.UriInfo;
import java.time.LocalDateTime;
import org.jboss.resteasy.reactive.server.ServerExceptionMapper;
import org.uallace.livebit.shared.ErrorResponse;

public class AuthExceptionsMapper {

    @ServerExceptionMapper
    public Response handleUserEmailAlreadyExistsException(UserEmailAlreadyExistsException ex, UriInfo uriInfo) {
        ErrorResponse<String> err = new ErrorResponse<>(
            LocalDateTime.now(),
            "Email already registered",
            uriInfo.getPath(),
            null
        );

        return Response.status(Response.Status.BAD_REQUEST.getStatusCode())
            .entity(err)
            .build();
    }

    @ServerExceptionMapper
    public Response handleUserUsernameAlreadyExistsException(UserUsernameAlreadyExistsException ex, UriInfo uriInfo) {
        ErrorResponse<String> err = new ErrorResponse<>(
            LocalDateTime.now(),
            "Username already registered",
            uriInfo.getPath(),
            null
        );

        return Response.status(Response.Status.BAD_REQUEST.getStatusCode())
            .entity(err)
            .build();
    }

    @ServerExceptionMapper
    public Response handleInvalidCredentialsException(InvalidCredentialsException ex, UriInfo uriInfo) {
        ErrorResponse<String> err = new ErrorResponse<>(
            LocalDateTime.now(),
            "Invalid credentials",
            uriInfo.getPath(),
            null
        );

        return Response.status(Response.Status.UNAUTHORIZED.getStatusCode())
            .entity(err)
            .build();
    }
}
