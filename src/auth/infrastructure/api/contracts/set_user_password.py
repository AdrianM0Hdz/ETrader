from dataclasses import dataclass


@dataclass(frozen=True)
class SetUserPasswordRequest:
    user_id: str
    password: str
