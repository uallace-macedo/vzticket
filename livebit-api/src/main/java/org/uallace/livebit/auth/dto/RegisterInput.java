package org.uallace.livebit.auth.dto;

import jakarta.validation.constraints.*;
import org.hibernate.validator.constraints.Length;
import org.uallace.livebit.user.UserRole;

public record RegisterInput(
        @NotBlank
        @Length(min=4, max=50)
        String username,

        @NotBlank
        @Email
        String email,

        @NotBlank
        @Size(min = 8, message = "password must be equal or greater than 8")
        String password,

        @NotNull
        UserRole role
) {}
