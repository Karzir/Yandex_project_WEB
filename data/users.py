import datetime
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    check_password = sqlalchemy.Column(sqlalchemy.String)
    progress = sqlalchemy.Column(sqlalchemy.Integer)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    photo = sqlalchemy.Column(sqlalchemy.String)
    lst_complete_task = sqlalchemy.Column(sqlalchemy.String)
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password1(self, password):
        return check_password_hash(self.hashed_password, password)
