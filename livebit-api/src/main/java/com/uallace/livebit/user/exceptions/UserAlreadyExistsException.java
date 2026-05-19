package com.uallace.livebit.user.exceptions;

public class UserAlreadyExistsException extends RuntimeException {
    public UserAlreadyExistsException(String field) {
        super(String.format("User already exists by field: %s", field));
    }

    public UserAlreadyExistsException() {
        super("User already exists");
    }
}
