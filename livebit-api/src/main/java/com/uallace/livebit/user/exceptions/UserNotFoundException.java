package com.uallace.livebit.user.exceptions;

import java.util.UUID;

public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(UUID id) {
        super(String.format("User with id '%s' not found", id.toString()));
    }

    public UserNotFoundException() {
        super("User not found");
    }
}
