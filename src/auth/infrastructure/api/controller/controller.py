from flask import Response, jsonify

from src.shared_kernel.infrastructure.api.controller import (
    Controller,
    handler,
    HTTPMethod,
)

from src.auth.application.commands import (
    SetUserPassword,
    VerifyUserPassword,
    RegisterUserCredentials,
)

from ..contracts import SetUserPasswordRequest, VerifyUserPasswordRequest


class AuthController(Controller):
    def __init__(
        self,
        set_user_password_service: SetUserPassword,
        verify_user_password_service: VerifyUserPassword,
        name: str = "auth",
        url_prefix: str = "/auth",
    ):
        super().__init__(name, url_prefix)

        self.set_user_password_service = set_user_password_service
        self.verify_user_password_service = verify_user_password_service

    @handler(SetUserPasswordRequest)
    def handle_set_user_password_request(
        self, request: SetUserPasswordRequest
    ) -> Response:
        ...

    @handler(VerifyUserPasswordRequest)
    def handle_verify_user_password_request(
        self, request: VerifyUserPasswordRequest
    ) -> Response:
        ...
