import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Answer(SqlAlchemyBase):
    __tablename__ = "answers"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)

    question_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("questions.id"))
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    json_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    question = orm.relation("Question")