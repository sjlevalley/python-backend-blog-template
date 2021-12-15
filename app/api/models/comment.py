from db import db
import uuid


class CommentModel(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80))
    author = db.Column(db.String(80))
    text = db.Column(db.String(80000))

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    article = db.relationship('ArticleModel')

    # votes = db.relationship('VoteModel', lazy='dynamic')

    def __init__(self, date, author, text, article_id):
        self.id = uuid.uuid4
        self.date = date
        self.author = author
        self.text = text
        self.article_id = article_id
    
    def __str__(self) -> str:
        return (f"Comment ID: {self.id} Article ID: {self.article_id}, Date: {self.date}, Author: {self.author}")

    def __str__(self) -> str:
        return f"<Comment({self.id}, {self.article_id}, {self.date}, {self.author})>"

    def json(self):
        return {
            'id': self.id,
            'date': self.date, 
            'author': self.author,
            'text': self.text,
            'article_id': self.article_id
            }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_author(cls, author):
        comments = cls.query.filter_by(author=author).all()
        return comments

    @classmethod
    def find_by_article(cls, article_id):
        comments = cls.query.filter_by(article_id=article_id).all()
        return comments

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()