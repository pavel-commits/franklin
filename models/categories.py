import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('courses_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('courses.id')),
    sqlalchemy.Column('category_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('categories.id'))
)


class Categories(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "categories"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    side_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("sides.id"), nullable=True)

    side = orm.relation("Sides")
    courses = orm.relation("Courses", secondary="association", back_populates="categories")