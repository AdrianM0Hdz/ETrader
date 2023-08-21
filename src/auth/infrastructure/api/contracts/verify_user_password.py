from dataclasses import dataclass


@dataclass(frozen=True)
class VerifyUserPasswordRequest:
    user_id: str
    password: str
