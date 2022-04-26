import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Sides(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "sides"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    json_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    categories = orm.relation("Categories", back_populates="side")