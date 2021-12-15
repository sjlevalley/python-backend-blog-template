from db import db
import uuid


class VoteModel(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80))
    user_id = db.Column(db.String(80))
    type = db.Column(db.String(80))

    article = db.relationship('ArticleModel')
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

    # votes = db.relationship('VoteModel', lazy='dynamic')

    def __init__(self, date, user_id, type, article_id):
        self.id = uuid.uuid4
        self.date = date
        self.user_id = user_id
        self.type = type
        self.article_id = article_id

    def json(self):
        return {
            'id': self.id,
            'date': self.date, 
            'user_id': self.user_id,
            'type': self.type,
            'article_id': self.article_id
            }
    
    def __str__(self) -> str:
        return (f"ID: {self.id}, Date: {self.date}, User ID: {self.user_id}, Type: {self.type}, Article ID: {self.article_id}")

    def __str__(self) -> str:
        return f"<User({self.id}, {self.date}, {self.user_id}, {self.type}, {self.article_id})>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_user(cls, user_id):
        votes = cls.query.filter_by(user_id=user_id).all()
        return votes

    @classmethod
    def find_by_article(cls, article_id):
        votes = cls.query.filter_by(article_id=article_id).all()
        return votes

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()