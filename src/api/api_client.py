from src.api.controllers import Users, Contacts
from src.api.request import Request


class APIClient:
    def __init__(self, request: Request):
        self.request: Request = request
        self.contacts: Contacts = Contacts(request)
        self.users: Users = Users(request)

    def authenticate(self, user_email: str, password: str) -> None:
        response = self.users.login(
            login_data={
                "email": user_email,
                "password": password
            }
        )
        self.request.set_token(response.json()["token"])
