package org.uallace.livebit.infra;

import io.smallrye.jwt.build.Jwt;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.core.NewCookie;
import org.eclipse.microprofile.config.inject.ConfigProperty;

@ApplicationScoped
public class TokenService {

    @Inject
    @ConfigProperty(name = "smallrye.jwt.verify.issuer")
    String issuer;

    @Inject
    @ConfigProperty(name = "quarkus.http.auth.cookie.cookie-name")
    String cookieName;

    @Inject
    @ConfigProperty(name = "quarkus.http.cors.origin")
    String clientUrl;

    public NewCookie generateCookie(String email, String role) {
        int MAX_AGE = 3600 * 5;

        String token = Jwt.issuer(issuer)
            .upn(email)
            .groups(role)
            .expiresIn(MAX_AGE)
            .sign();

        return new NewCookie.Builder(cookieName)
            .value(token)
            .path("/")
            .secure(clientUrl.startsWith("https"))
            .maxAge(MAX_AGE)
            .build();
    }
}
