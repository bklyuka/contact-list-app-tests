from typing import Any, List

from src.api.controller_registry import controller_classes
from src.api.controllers import UserAPI
from src.api.request import Request


class APIClient:
    def __init__(self, request: Request):
        self._request: Request = request
        self._controllers: List[Any] = []

        for name, cls in controller_classes.items():
            instance = cls(request)
            setattr(self, name, instance)
            self._controllers.append(instance)

    def __getattr__(self, name: str) -> Any:
        for controller in self._controllers:
            if hasattr(controller, name):
                return getattr(controller, name)
        raise AttributeError(f"No attribute `{name}`")

    def authenticate(self, user_email: str, password: str) -> None:
        response = UserAPI(self._request).login(
            login_data={
                "email": user_email,
                "password": password
            }
        )
        self._request.set_token(response.json()["token"])
