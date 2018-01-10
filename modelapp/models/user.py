from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique = True)
    password = db.Column(db.String(32))

    def register(self, username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            return False
        return True
    
    def login(self, username, password):
        user = self.getUser(username)
        if user and user.password == password:
            return True
        return False

    
    def getUser(self, username):
        try: 
            return User.query.filter_by(username=username).one()
        except NoResultFound:
            return False


