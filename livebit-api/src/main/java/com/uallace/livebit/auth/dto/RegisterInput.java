package com.uallace.livebit.auth.dto;

import com.uallace.livebit.user.UserRole;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.hibernate.validator.constraints.Length;

public record RegisterInput(
        @NotBlank @Email String email,
        @NotBlank String username,
        @NotBlank @Length(min = 8, message = "Password must have at least 8 chars") String password,
        @NotNull UserRole role
) {}
