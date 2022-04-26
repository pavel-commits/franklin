import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Tests(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "tests"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    results = orm.relation("Results", back_populates="test")
    questions = orm.relation("Question", back_populates="test")