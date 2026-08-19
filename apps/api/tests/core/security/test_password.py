from verzel.core.security.password import generate_hash, verify_password


def test_generate_hash_success():
    password = 'simple-password'
    hashed_password = generate_hash(password)

    assert hashed_password
    assert password != hashed_password

    second_hashed_password = generate_hash(password)
    assert hashed_password != second_hashed_password


def test_verify_password_correct():
    password = 'simple-password'
    hashed_password = generate_hash(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_incorrect():
    password = 'simple-password'
    hashed_password = generate_hash(password)

    assert verify_password('wrong-password', hashed_password) is False
