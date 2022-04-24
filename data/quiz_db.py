import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Quiz(SqlAlchemyBase):
    __tablename__ = 'quiz'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relation('User')
