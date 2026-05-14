package org.uallace.livebit.user.dto;

import org.uallace.livebit.user.UserRole;

import java.util.UUID;

public record UserDTO(
        UUID id,
        String username,
        String email,
        UserRole role
) {}
