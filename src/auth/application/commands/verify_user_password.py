from src.auth.domain.user_credentials.repository import UserCredentialsRepository
from src.auth.domain.user_credentials.values import UserCredentialsId
from src.auth.domain.user_credentials.enums import PasswordVerificationResult


class VerifyUserPassword:
    def __init__(self, user_credentials_repository: UserCredentialsRepository):
        self.user_credentials_repository = user_credentials_repository

    def __call__(
        self, raw_user_credentials_id: str, raw_password: str
    ) -> PasswordVerificationResult:
        user_credentials_id = UserCredentialsId(raw_user_credentials_id)
        user_credentials = self.user_credentials_repository.get(user_credentials_id)
        return user_credentials.verify_password(raw_password)
