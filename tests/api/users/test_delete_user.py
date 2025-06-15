from http import HTTPStatus

import pytest
from assertpy import assert_that

from src.api.api_client import APIClient
from src.errors import CommonErrors


class TestAPIDeleteUser:

    @pytest.mark.testomatio("@T8ef4b4f4")
    @pytest.mark.api
    def test_delete_user_me_successfully(self, client: APIClient) -> None:
        response = client.delete_user_me()

        assert response.status == HTTPStatus.OK
        assert_that(response.text()).is_empty()

    @pytest.mark.testomatio("@Tdc6f1494")
    @pytest.mark.api
    def test_delete_user_me_without_token_provided(self, unauth_client: APIClient) -> None:
        response = unauth_client.delete_user_me()
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
