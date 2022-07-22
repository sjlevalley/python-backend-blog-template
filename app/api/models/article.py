from db import db
import uuid
from models.vote import VoteModel
from models.comment import CommentModel


class ArticleModel(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    subtitle = db.Column(db.String(80))
    date = db.Column(db.String(80))
    author = db.Column(db.String(80))
    text = db.Column(db.String(80000))

    comments = db.relationship(CommentModel, lazy='dynamic', overlaps="article")
    votes = db.relationship(VoteModel, lazy='dynamic', overlaps="article")

    def __init__(self, title, subtitle, date, author, text):
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.author = author
        self.text = text

    def __str__(self) -> str:
        return (f"Article ID: {self.id}, Article Title: {self.title}, Subtitle: {self.subtitle}, Date: {self.date}, Author: {self.author}")

    def __repr__(self) -> str:
        return f"<Article({self.id}, {self.title}, {self.subtitle}, {self.date}, {self.author})>"

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'date': self.date,
            'author': self.author,
            'text': self.text,
            'votes': [vote.json() for vote in self.votes.all()],
            'comments': [comment.json() for comment in self.comments.all()]
            }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
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