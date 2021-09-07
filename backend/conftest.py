import pytest
from rest_framework.test import APIClient

from tests.defaults import DEFAULT_USER_PARAMS, DEFAULT_USER_2_PARAMS


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(**DEFAULT_USER_PARAMS)


@pytest.fixture
def user2(django_user_model):
    return django_user_model.objects.create(**DEFAULT_USER_2_PARAMS)


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    response = client.post(
        path="/users/login/",
        data={
            "email": user.email,
            "password": "member_password",
        },
    )
    assert 200 == response.status_code
    client.defaults.update(HTTP_AUTHORIZATION=f'Bearer {response.data.get("access")}')
    return client


@pytest.fixture
def authenticated_client2(user2):
    client = APIClient()
    response = client.post(
        path="/users/login/",
        data={
            "email": user2.email,
            "password": "member_password",
        },
    )
    assert 200 == response.status_code
    client.defaults.update(HTTP_AUTHORIZATION=f'Bearer {response.data.get("access")}')
    return client
