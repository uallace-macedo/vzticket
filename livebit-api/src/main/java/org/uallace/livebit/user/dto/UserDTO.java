package org.uallace.livebit.user.dto;

import java.util.UUID;
import org.uallace.livebit.user.UserRole;

public record UserDTO(UUID id, String username, String email, UserRole role) {}
