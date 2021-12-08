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

    comments = db.relationship(CommentModel, lazy='dynamic')
    votes = db.relationship(VoteModel, lazy='dynamic')

    def __init__(self, title, subtitle, date, author, text):
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.author = author
        self.text = text
        

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()