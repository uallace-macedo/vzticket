package com.uallace.livebit.auth.dto;

import java.util.UUID;

public record RegisterOutput(
        UUID id,
        String username,
        String email
) {}
