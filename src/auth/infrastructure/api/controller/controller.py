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


class AuthController(Controller):
    def __init__(
        self,
        set_user_password_service: SetUserPassword,
        verify_user_password_service: VerifyUserPassword,
        register_user_credentials_service: RegisterUserCredentials,
        name: str = "auth",
        url_prefix: str = "/auth",
    ):
        super().__init__(name, url_prefix)

        self.set_user_password_service = set_user_password_service
        self.verify_user_password_service = verify_user_password_service
        self.register_user_credentials_service = register_user_credentials_service
