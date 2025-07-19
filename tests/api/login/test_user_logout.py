from http import HTTPStatus

import pytest
from assertpy import assert_that

from src.api.user_api import UserApi
from src.errors import CommonErrors
from src.payloads import CreateUser, LoginCredentials


@pytest.fixture(name="credentials")
def get_creds_of_new_user(user_api: UserApi) -> LoginCredentials:
    credentials_ = LoginCredentials()

    user_api.create(
        user_data=CreateUser(
            email=credentials_.email,
            password=credentials_.password
        ).__dict__
    )
    return credentials_


@pytest.fixture(name="client")
def get_authenticated_new_client(user_api: UserApi, credentials: LoginCredentials) -> UserApi:
    user_api.authenticate(
        user_email=credentials.email,
        password=credentials.password
    )
    return user_api


class TestAPIUserLogout:

    @pytest.mark.testomatio("@T670d7605")
    @pytest.mark.api
    def test_logout_successfully(self, client: UserApi) -> None:
        response = client.logout()

        assert response.status == HTTPStatus.OK
        assert_that(response.text()).is_empty()

    @pytest.mark.testomatio("@Tf8391138")
    @pytest.mark.api
    def test_logout_for_not_authenticated_client(self, user_api: UserApi) -> None:
        response = user_api.logout()
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
