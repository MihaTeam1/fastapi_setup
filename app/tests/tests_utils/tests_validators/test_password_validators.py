import pytest

from settings import settings
from utils.validators.password import (
    MinLengthValidator,
    SimilarPasswordUsernameValidator,
    ComparePasswordsValidator,
    ASCIIPasswordValidator,
)
from exceptions import ValidationError

PASSWORD_VALIDATOS = getattr(settings, 'password_validators')


def test_min_length_validator_fail():
    validator = None
    for val in PASSWORD_VALIDATOS:
        if isinstance(val, MinLengthValidator):
            validator = val
            break
    else:
        pytest.skip()
    try:
        validator('#'*(validator.min_length-1))
        raise AssertionError(
            f'Minimal password length = {validator.min_length}, '
            f'given password was length = {validator.min_length - 1} '
            'and validator passed it'
        )
    except ValidationError:
        pass
    for length in range(1,50):
        validator = MinLengthValidator(length)
        try:
            validator('#' * (validator.min_length - 1))
            raise AssertionError(
                f'Minimal password length = {validator.min_length}, '
                f'given password was length = {validator.min_length - 1} '
                'and validator passed it'
            )
        except ValidationError:
            pass


def test_min_length_validator_success():
    validator = None
    for val in PASSWORD_VALIDATOS:
        if isinstance(val, MinLengthValidator):
            validator = val
            break
    else:
        pytest.skip()
    try:
        for i in range(10):
            validator('#'*(validator.min_length+i))
    except ValidationError:
        raise AssertionError(
            f'Minimal password length = {validator.min_length}, '
            f'given password was length = {validator.min_length} '
            'and validator failed it'
        )
    for length in range(1,50):
        validator = MinLengthValidator(length)
        try:
            for i in range(10):
                validator('#' * (validator.min_length + i))
        except ValidationError:
            raise AssertionError(
                f'Minimal password length = {validator.min_length}, '
                f'given password was length = {validator.min_length} '
                'and validator failed it'
            )


def test_similarity_password_username_fail():
    validator = None
    for val in PASSWORD_VALIDATOS:
        if isinstance(val, SimilarPasswordUsernameValidator):
            validator = val
            break
    else:
        pytest.skip()
    ratio = validator.ratio
    tests = {
        1: {'username': 'testtest', 'password': 'testtest'},
        0.9: {'username': 'testtest', 'password': 'testtes1t'},
        0.8: {'username': 'testtest', 'password': 'testtes1t12'},
        0.7: {'username': 'testtest', 'password': 'testtes1t1234'},
        0.6: {'username': 'testtest', 'password': 'testtes1t123456'},
        0.5: {'username': 'testtest', 'password': 'testtes1t1234567890'},
        0.4: {'username': 'testtest', 'password': '12345678esttest123456789'},
        0.3: {'username': 'testtest', 'password': '1234test12345'},
        0.2: {'username': 'testtest', 'password': 'tefd123fgh1'},
    }
    for test_ratio in tests:
        try:
            if ratio <= test_ratio:
                validator(**tests[test_ratio])
                raise AssertionError(
                    f'test_ratio is {test_ratio} and similarity validator with ratio {ratio} passed it'
                )
        except ValidationError:
            pass
    for i in range(1,11):
        ratio = i/10
        validator = SimilarPasswordUsernameValidator(ratio)
        for test_ratio in tests:
            try:
                if ratio <= test_ratio:
                    validator(**tests[test_ratio])
                    raise AssertionError(
                        f'test_ratio is {test_ratio} and similarity validator with ratio {ratio} passed it'
                    )
            except ValidationError:
                pass


def test_similarity_password_username_success():
    validator = None
    for val in PASSWORD_VALIDATOS:
        if isinstance(val, SimilarPasswordUsernameValidator):
            validator = val
            break
    else:
        pytest.skip()
    ratio = validator.ratio
    tests = {
        1: {'usename': 'testtest', 'password': 'testtes1t'},
        0.9: {'username': 'testtest', 'password': 'testtes1t12'},
        0.8: {'username': 'testtest', 'password': 'testtes1t1234'},
        0.7: {'username': 'testtest', 'password': 'testtes1t123456'},
        0.6: {'username': 'testtest', 'password': 'testtes1t1234567890'},
        0.5: {'username': 'testtest', 'password': '12345678esttest123456789'},
        0.4: {'username': 'testtest', 'password': '1234test12345'},
        0.3: {'username': 'testtest', 'password': 'tefd123fgh1'},
        0.2: {'username': 'testtest', 'password': 'fghe'},
    }
    for test_ratio in tests:
        try:
            if ratio > test_ratio:
                validator(**tests[test_ratio])
        except ValidationError:
            raise AssertionError(
                f'test_ratio is {test_ratio} and similarity validator with ratio {ratio} failed it'
            )
    for i in range(1,11):
        ratio = i/10
        validator = SimilarPasswordUsernameValidator(ratio)
        for test_ratio in tests:
            try:
                if ratio > test_ratio:
                    validator(**tests[test_ratio])
            except ValidationError:
                raise AssertionError(
                    f'test_ratio is {test_ratio} and similarity validator with ratio {ratio} failed it'
                )

