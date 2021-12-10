# Add Try/Catches

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister, UserList, UserByID, UserByUsername
from resources.comment import CommentByID, CommentByAuthor ,CommentList, CommentByArticle
from resources.article import ArticleByTitle, ArticleList, ArticleByID
from resources.vote import VoteList, VoteByUserID, VoteByID, VoteByArticle

from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'steve'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(ArticleList, '/api/articles')
api.add_resource(ArticleByTitle, '/api/articles/title/<string:title>')
api.add_resource(ArticleByID, '/api/articles/id/<string:id>')

api.add_resource(CommentList, '/api/comments')
api.add_resource(CommentByID, '/api/comments/<string:id>')
api.add_resource(CommentByAuthor, '/api/comments/users/<string:author>')
api.add_resource(CommentByArticle, '/api/articles/<string:article_id>/comments')

api.add_resource(VoteList, '/api/votes')
api.add_resource(VoteByUserID, '/api/users/<string:user_id>/votes')
api.add_resource(VoteByArticle, '/api/articles/<string:id>/votes')
api.add_resource(VoteByID, '/api/votes/<string:id>')

api.add_resource(UserList, '/api/users')
api.add_resource(UserByID, '/api/users/id/<string:id>')
api.add_resource(UserByUsername, '/api/users/username/<string:username>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)