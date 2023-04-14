import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Expenses(SqlAlchemyBase):
    __tablename__ = 'expenses'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    def __repr__(self):
        return f"{self.title}: {self.money[:10]}... / {self.created_date.strftime('%d.%m.%y %H:%M')}"
