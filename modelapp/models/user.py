from flask import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))

    def getUser(self, username):
        try:
            return User.query.filter_by(username=username).one()
        except NoResultFound:
            pass

    def checkUser(self, username, passwd):
        user = self.getUser(username)
        if user:
            if user.password == passwd:
                return True
        return False

    def addUser(self, username, passwd):
        user = User(username=username, password=passwd)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            return False
        return True
