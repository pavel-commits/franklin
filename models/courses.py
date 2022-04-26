import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Courses(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "courses"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    brand = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    workability = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    long = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    categories = orm.relation("Categories", secondary="association", back_populates="courses")

