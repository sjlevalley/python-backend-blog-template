# Add Try/Catches

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST

from resources.user import UserRegister, UserList, UserByID, UserByUsername, UserLogin, TokenRefresh, UserLogout
from resources.comment import CommentByID, CommentByAuthor ,CommentList, CommentByArticle
from resources.article import ArticleByTitle, ArticleList, ArticleByID
from resources.vote import VoteList, VoteByUserID, VoteByID, VoteByArticle


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLOCKLIST_ENABLED'] = True
app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] # Enables blacklist for both access and refresh tokens
app.secret_key = 'steve' # can use app.config['JWT_SECRET_KEY']
api = Api(app)


@app.before_first_request # Runs this command before initial request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # Should actually be read from a config file or database
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blocklist_loader # Check to see if token is in the Blocklist
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    print(jwt_payload)
    user_id = jwt_payload['jti']
    return user_id in BLOCKLIST

@jwt.expired_token_loader # Tells Flask what message to return to the user if the token is expired
def expired_token_loader(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Your Token has expired',
        'error': 'token_expired'
    }), 401

@jwt.revoked_token_loader # Returns message after token has been revoked (user logged out)
def revoked_token_response(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Your Token has been revoked',
        'error': 'token_revoked'
    }), 401

@jwt.invalid_token_loader # Returns message when token is invalid
def invalid_token_response(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader # Returns message when token does not contain proper auth level
def unauthorized_response(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Your Token does not have proper authorization',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader # Returns message when token is not fresh but fresh token is required
def needs_fresh_token_response(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Token not fresh',
        'error': 'fresh_token_required'
    }), 401

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
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserRegister, '/register')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)