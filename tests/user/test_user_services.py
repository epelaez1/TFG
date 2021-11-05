import pytest

from src.user.user_services import register_user
from src.user.domain.user_repository import UserRepository
from src.user.domain.user_exceptions import UserAlreadyRegistered

sample_user = {
    'email': 'new_user@mail.es',
    'name': 'bob',
    'phone': '6543213210'
}


def test_new_user_register(user_repository: UserRepository):
    new_user = register_user(**sample_user, user_repository=user_repository)
    assert user_repository.has(new_user.email)


def test_register_existing_user_raise_exception(user_repository: UserRepository):
    register_user(**sample_user, user_repository=user_repository)
    with pytest.raises(UserAlreadyRegistered):
        register_user(**sample_user, user_repository=user_repository)
