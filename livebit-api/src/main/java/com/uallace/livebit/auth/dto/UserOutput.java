package com.uallace.livebit.auth.dto;

import com.uallace.livebit.user.UserRole;

public record UserOutput(
        String username,
        String email,
        UserRole role
) {}
