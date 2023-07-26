from enum import Enum


class PasswordVerificationResult(Enum):
    INCORRECT_PASSWORD = "INCORRECT_PASSWORD"
    CORRECT_PASSWORD = "CORRECT_PASSWORD"
