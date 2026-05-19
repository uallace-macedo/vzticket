package com.uallace.livebit.auth;

import com.uallace.livebit.auth.dto.LoginInput;
import com.uallace.livebit.auth.dto.LoginOutput;
import com.uallace.livebit.auth.dto.RegisterInput;
import com.uallace.livebit.auth.dto.RegisterOutput;
import com.uallace.livebit.auth.exceptions.InvalidCredentialsException;
import com.uallace.livebit.infra.security.TokenService;
import com.uallace.livebit.user.UserEntity;
import com.uallace.livebit.user.UserRepository;
import com.uallace.livebit.user.exceptions.UserAlreadyExistsException;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final TokenService tokenService;

    public RegisterOutput register(RegisterInput input) {
        if(userRepository.findByEmail(input.email()).isPresent()) throw  new UserAlreadyExistsException("email");

        UserEntity user = new UserEntity();
        user.setEmail(input.email());
        user.setName(input.username());
        user.setPassword(passwordEncoder.encode(input.password()));
        user.setRole(input.role());

        UserEntity saved = userRepository.save(user);
        return new RegisterOutput(
                saved.getId(),
                saved.getEmail(),
                saved.getUsername()
        );
    }

    public LoginOutput login(LoginInput input, HttpServletResponse response) {
        var authenticationToken = new UsernamePasswordAuthenticationToken(
                input.email(),
                input.password()
        );

        Authentication authentication = authenticationManager.authenticate(authenticationToken);
        UserEntity user = (UserEntity) authentication.getPrincipal();
        String token = tokenService.generateToken(user);

        return new LoginOutput(
                user.getName(),
                user.getEmail(),
                user.getRole(),
                token
        );
    }
}
