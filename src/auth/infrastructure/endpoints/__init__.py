from flask import Blueprint, jsonify

from src.auth.application.commands.verify_user_password import VerifyUserPassword
from ..persistence.user_credentials.mongodb.repository import (
    MongoDBUserCredentialsRepository,
)

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/verify_user_password", methods=["POST"])
def verify_user_password():
    return jsonify()
