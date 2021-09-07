from types import MappingProxyType
from typing import Mapping, Union, Any

from django.contrib.auth.hashers import make_password

DEFAULT_USER_PARAMS: Mapping[str, Union[Any]] = MappingProxyType(
    {
        "email": "member@messages.com",
        "username": "member",
        "password": make_password("member_password"),
        "is_staff": False,
        "is_superuser": False,
    }
)
DEFAULT_USER_2_PARAMS: Mapping[str, Union[Any]] = MappingProxyType(
    {
        "email": "member2@messages.com",
        "username": "member2",
        "password": make_password("member_password"),
        "is_staff": False,
        "is_superuser": False,
    }
)

DEFAULT_REGISTER_PARAMS: Mapping[str, str] = MappingProxyType(
    {
        "email": "member@messages.com",
        "username": "member",
        "password1": "member_password",
        "password2": "member_password",
    }
)
