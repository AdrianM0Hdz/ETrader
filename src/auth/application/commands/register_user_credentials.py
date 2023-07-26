from src.auth.domain.user_credentials import UserCredentials
from src.auth.domain.user_credentials.values import PasswordHash, UserId
from src.auth.domain.user_credentials.repository import UserCredentialsRepository


class RegisterUserCredentials:
    def __init__(self, user_credentials_repository: UserCredentialsRepository):
        self.user_credentials_repository = user_credentials_repository

    def __call__(self, raw_user_id: str, raw_password: str):
        user_credentials = UserCredentials.create_new(
            UserId(raw_user_id), PasswordHash(raw_password)
        )
        self.user_credentials_repository.add(user_credentials)
