import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Quiz(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'quiz'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    questions = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    owner_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("user.id"),
                                 nullable=True)

    passers = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relation('User')

# тут тоже можно изменить
