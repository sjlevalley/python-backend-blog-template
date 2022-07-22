from db import db
import uuid

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __str__(self) -> str:
        return f"ID: {self.id} Username: {self.username}, Email: {self.email}"

    def __str__(self) -> str:
        return f"<User({self.id}, {self.username}, {self.email})>"

    def json(self):  ## Be sure to erase the 'password' field on line 21 before use, I just left this in here for testing!
        return {
            'id': self.id,
            'username': self.username, 
            'password': self.password, # Generally don't want to have this visible
            'email': self.email            
            }
  
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()