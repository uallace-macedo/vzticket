package com.uallace.livebit.auth;

import com.uallace.livebit.auth.dto.LoginInput;
import com.uallace.livebit.auth.dto.LoginOutput;
import com.uallace.livebit.auth.dto.RegisterInput;
import com.uallace.livebit.auth.dto.RegisterOutput;
import com.uallace.livebit.infra.security.TokenService;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
public class AuthController {
    private final AuthService authService;
    private final TokenService tokenService;

    @PostMapping("/register")
    public ResponseEntity<RegisterOutput> register(@RequestBody @Valid RegisterInput input) {
        RegisterOutput user = authService.register(input);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }

    @PostMapping("/login")
    public ResponseEntity<LoginOutput> login(@RequestBody @Valid LoginInput input, HttpServletResponse response) {
        LoginOutput user = authService.login(input);

        Cookie cookie = new Cookie(tokenService.getCookieName(), user.token());
        cookie.setHttpOnly(true);
        cookie.setSecure(tokenService.getSecure());
        cookie.setPath("/");
        cookie.setMaxAge(tokenService.getExpiresIn());

        response.addCookie(cookie);
        return ResponseEntity.ok().body(user);
    }

    @PostMapping("/logout")
    public ResponseEntity<LoginOutput> logout(HttpServletResponse response) {
        Cookie cookie = new Cookie(tokenService.getCookieName(), "");
        cookie.setHttpOnly(true);
        cookie.setSecure(tokenService.getSecure());
        cookie.setPath("/");
        cookie.setMaxAge(0);

        response.addCookie(cookie);
        return ResponseEntity.ok().build();
    }
}
