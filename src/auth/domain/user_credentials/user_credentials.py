from uuid import uuid1

from src.shared_kernel.domain.aggregate_root import AggregateRoot

from .values import UserCredentialsId, PasswordHash, UserId
from .enums import PasswordVerificationResult


class UserCredentials(AggregateRoot[UserCredentialsId]):
    def __init__(
        self, id: UserCredentialsId, user_id: UserId, password_hash: PasswordHash
    ):
        super().__init__(id)
        assert isinstance(user_id, UserId)
        assert isinstance(password_hash, PasswordHash)
        self.password_hash = password_hash
        self.user_id = user_id

    def verify_password(self, raw_password: str) -> PasswordVerificationResult:
        password_hash = PasswordHash(raw_password)
        if self.password_hash == password_hash:
            return PasswordVerificationResult.CORRECT_PASSWORD
        return PasswordVerificationResult.INCORRECT_PASSWORD

    @classmethod
    def create_new(cls, user_id: UserId, password: PasswordHash):
        id = UserCredentialsId(str(uuid1()))
        return cls(id, user_id, password)
