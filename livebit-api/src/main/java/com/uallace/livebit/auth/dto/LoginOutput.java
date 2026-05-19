package com.uallace.livebit.auth.dto;

import com.uallace.livebit.user.UserRole;

public record LoginOutput(
        String username,
        String email,
        UserRole role,
        String token
) {}
