from pymongo.collection import Collection
from src.auth.domain.user_credentials import UserCredentials
from src.auth.domain.user_credentials.user_credentials import UserCredentials
from src.auth.domain.user_credentials.values import (
    UserCredentialsId,
    UserId,
    PasswordHash,
)
from src.auth.domain.user_credentials.repository import UserCredentialsRepository


class MongoDBUserCredentialsRepository(UserCredentialsRepository):
    def __init__(self, user_credentials_collection: Collection):
        self.user_credentials_collection = user_credentials_collection

    def _serialize_user_credentials(self, item: UserCredentials) -> dict:
        return {
            "id": item.id.value,
            "userId": item.user_id.value,
            "passwordHash": item.password_hash.value if item.password_hash else None,
        }

    def _deserialize_user_credentials(self, raw_item: dict) -> UserCredentials:
        return UserCredentials(
            id=UserCredentialsId(raw_item["id"]),
            user_id=UserId(raw_item["userId"]),
            password_hash=PasswordHash(raw_item["passwordHash"])
            if raw_item["passwordHash"]
            else None,
        )

    def _user_credentials_already_exist(self, user_credentials: UserCredentials):
        raw_user_credentials = self.user_credentials_collection.find_one(
            {"id": user_credentials.id.value}
        )
        if raw_user_credentials is not None:
            return True
        return False

    def add(self, item: UserCredentials):
        if self._user_credentials_already_exist(item):
            raise ValueError("User Credentials with that id already exist")
        serialized_item = self._serialize_user_credentials(item)
        self.user_credentials_collection.insert_one(serialized_item)

    def get(self, id: UserCredentialsId):
        serialized_item = self.user_credentials_collection.find_one({"id": id.value})
        if serialized_item is None:
            raise ValueError("UserCredentials with that id does not exist")
        return self._deserialize_user_credentials(serialized_item)

    def get_by_user_id(self, user_id: UserId) -> UserCredentials:
        serialized_item = self.user_credentials_collection.find_one(
            {"userId": user_id.value}
        )
        if serialized_item is None:
            raise ValueError("UserCredentials with that id does not exist")
        return self._deserialize_user_credentials(serialized_item)

    def commit(self, item: UserCredentials):
        if not self._user_credentials_already_exist(item):
            raise ValueError("cannot commit user credentials that do not exist")
        self.user_credentials_collection.update_one(
            {"id": item.id.value},
            {
                "$set": {
                    "passwordHash": item.password_hash.value
                    if item.password_hash
                    else None
                }
            },
        )

    def delete(self, item: UserCredentials):
        raise NotImplementedError()
