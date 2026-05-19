package com.uallace.livebit.infra.security;

import com.uallace.livebit.user.UserEntity;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Getter
public class TokenService {
    private final JwtEncoder jwtEncoder;

    @Value("${api.security.jwt.issuer}")
    private String issuer;

    @Value("${api.security.jwt.expiration-time}")
    private int expiresIn;

    @Value("${api.security.jwt.cookie-name}")
    private String cookieName;

    public String generateToken(UserEntity user) {
        Instant now = Instant.now();

        String scopes = user.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.joining(" "));

        JwtClaimsSet claims = JwtClaimsSet.builder()
                .issuer(issuer)
                .subject(user.getId().toString())
                .issuedAt(now)
                .expiresAt(now.plusSeconds((long) expiresIn))
                .claim("email", user.getEmail())
                .claim("scp", scopes)
                .build();

        return jwtEncoder.encode(JwtEncoderParameters.from(claims)).getTokenValue();
    }

    public boolean getSecure() {
        return this.issuer.startsWith("https");
    }
}
