package org.uallace.livebit.auth;

import jakarta.annotation.security.PermitAll;
import jakarta.validation.Valid;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.NewCookie;
import jakarta.ws.rs.core.Response;
import org.uallace.livebit.auth.dto.LoginInput;
import org.uallace.livebit.auth.dto.RegisterInput;
import org.uallace.livebit.infra.TokenService;
import org.uallace.livebit.user.UserEntity;
import org.uallace.livebit.user.UserMapper;

@Path("/api/v1/auth")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class AuthController {


    private final AuthService authService;
    private final TokenService tokenService;

    public AuthController(AuthService authService, TokenService tokenService) {
        this.authService = authService;
        this.tokenService = tokenService;
    }

    @POST
    @Path("/register")
    @PermitAll
    public Response register(@Valid RegisterInput input) {
        UserEntity userEntity = new UserEntity();
        userEntity.username = input.username();
        userEntity.email = input.email();
        userEntity.password = input.password();
        userEntity.role = input.role();

        var user = authService.register(userEntity);
        return Response
                .status(Response.Status.CREATED)
                .entity(UserMapper.toDto(user))
                .build();
    }

    @POST
    @Path("/login")
    @PermitAll
    public Response login(@Valid LoginInput input) {
        var user = authService.login(input.email(), input.password());
        NewCookie cookie = tokenService.generateCookie(user.email, user.role.name());

        return Response
                .status(Response.Status.OK)
                .cookie(cookie)
                .entity(UserMapper.toDto(user))
                .build();
    }
}
