from src.auth.domain.user_credentials.repository import UserCredentialsRepository
from src.auth.domain.user_credentials.values import UserId


class SetUserPassword:
    def __init__(self, user_credentials_repository: UserCredentialsRepository):
        self.user_credentials_repository = user_credentials_repository

    def __call__(self, raw_user_id: str, raw_password: str):
        user_credentials = self.user_credentials_repository.get_by_user_id(
            UserId(raw_user_id)
        )
        user_credentials.set_password(raw_password=raw_password)
        self.user_credentials_repository.commit(user_credentials)
