from flask import Response, jsonify

from src.shared_kernel.infrastructure.api.controller import (
    Controller,
    handler,
    HTTPMethod,
    success,
)

from src.auth.application.commands import (
    SetUserPassword,
    VerifyUserPassword,
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

        self.add_route(
            "/set_user_password",
            self.handle_set_user_password_request,
            HTTPMethod.POST,
        )

        self.add_route(
            "/verify_user_password",
            self.handle_verify_user_password_request,
            HTTPMethod.POST,
        )

    @handler(SetUserPasswordRequest)
    def handle_set_user_password_request(
        self, request: SetUserPasswordRequest
    ) -> Response:
        try:
            self.set_user_password_service(
                raw_user_id=request.user_id, raw_password=request.password
            )
            return success
        except BaseException as e:
            return jsonify(msg=str(e))

    @handler(VerifyUserPasswordRequest)
    def handle_verify_user_password_request(
        self, request: VerifyUserPasswordRequest
    ) -> Response:
        try:
            self.verify_user_password_service(
                raw_user_id=request.user_id, raw_password=request.password
            )
            return success
        except BaseException as e:
            return jsonify(msg=str(e))
