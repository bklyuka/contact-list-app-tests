# import pytest
#
# # from src.api.api_client import APIClient
# from src.payloads import CreateUser, LoginCredentials
#
#
# @pytest.fixture(name="credentials")
# def get_creds_of_new_user(unauth_client: APIClient) -> LoginCredentials:
#     credentials_ = LoginCredentials()
#
#     unauth_client.create_user(
#         user_data=CreateUser(
#             email=credentials_.email,
#             password=credentials_.password
#         ).__dict__
#     )
#     return credentials_
#
#
# @pytest.fixture(name="client")
# def get_authenticated_new_client(unauth_client: APIClient, credentials: LoginCredentials) -> APIClient:
#     unauth_client.authenticate(
#         user_email=credentials.email,
#         password=credentials.password
#     )
#     return unauth_client
