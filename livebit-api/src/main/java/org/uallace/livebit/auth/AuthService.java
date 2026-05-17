package org.uallace.livebit.auth;

import io.quarkus.elytron.security.common.BcryptUtil;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.transaction.Transactional;
import java.util.Optional;
import org.uallace.livebit.auth.exceptions.InvalidCredentialsException;
import org.uallace.livebit.auth.exceptions.UserEmailAlreadyExistsException;
import org.uallace.livebit.user.UserEntity;

@ApplicationScoped
public class AuthService {

    private Optional<UserEntity> findUserByEmail(String email) {
        return UserEntity.find("email", email).firstResultOptional();
    }

    @Transactional
    public UserEntity register(UserEntity userEntity) {
        if (findUserByEmail(userEntity.email).isPresent()) throw new UserEmailAlreadyExistsException();
        if (UserEntity.find("username", userEntity.username).firstResult() != null) throw new UserEmailAlreadyExistsException();

        userEntity.password = BcryptUtil.bcryptHash(userEntity.password);
        UserEntity.persist(userEntity);
        return userEntity;
    }

    public UserEntity login(String email, String password) {
        var user = findUserByEmail(email).orElseThrow(InvalidCredentialsException::new);
        if (BcryptUtil.matches(password, user.password)) return user;
        throw new InvalidCredentialsException();
    }
}
