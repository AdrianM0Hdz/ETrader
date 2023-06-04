from flask_sqlalchemy import SQLAlchemy

from .....domain.buyer.repository import BuyerRepository


class SQLAlchemyBuyerRepository(BuyerRepository):
    def __init__(self, db: SQLAlchemy):
        assert isinstance(db, SQLAlchemy)
        self.db = db
