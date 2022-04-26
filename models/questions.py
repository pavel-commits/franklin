import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = "questions"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)

    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tests.id"))
    question = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    test = orm.relation("Tests")
    answers = orm.relation("Answer", back_populates="question")
