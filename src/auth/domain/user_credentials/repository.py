from abc import abstractmethod

from shared_kernel.domain.repository import Repository

from .user_credentials import UserCredentials
from .values import UserCredentialsId, UserId


class UserCredentialsRepository(Repository):
    @abstractmethod
    def add(self, item: UserCredentials):
        ...

    @abstractmethod
    def get(self, id: UserCredentialsId) -> UserCredentials:
        ...

    @abstractmethod
    def get_by_user_id(self, id: UserId) -> UserCredentials:
        ...

    @abstractmethod
    def commit(self, item: UserCredentials):
        ...

    @abstractmethod
    def delete(self, item: UserCredentials):
        ...
