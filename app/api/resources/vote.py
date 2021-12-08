from flask_restful import Resource, reqparse, request
import json
from flask_jwt import jwt_required
from models.vote import VoteModel


class VoteByID(Resource):
    # @jwt_required()
    def get(self, id):
        vote = VoteModel.find_by_id(id)
        if not vote:
            return {'message': f'vote with id: {id} not found'}, 404
        return vote.json(), 200
        
    def delete(self, id):
        vote = VoteModel.find_by_id(id)
        if vote is None:
            return {'message': f'No vote found with id: {id}!'}, 404

        vote.delete_from_db()
        return {'message': 'Vote deleted!'}, 200

class VoteByUserID(Resource):
    # @jwt_required()
    def get(self, user_id):
        try: 
            votes = VoteModel.find_by_user(user_id)
        except:
            return {"message": "An error occurred when fetching votes for this user."}, 500

        if not votes:
            return {'message': f'No votes by author: {user_id} found!'}, 404

        return [vote.json() for vote in votes]
        
    def delete(self, author):
        votes = VoteModel.find_by_author(author)

        if len(votes) == 0:
            return {'message': f'No vote found with author: {author}!'}, 404

        for vote in votes:
            vote.delete_from_db()
            
        return {'message': f'All votes by author: {author} deleted!'}, 200


class VoteByArticle(Resource):

    # @jwt_required()
    def get(self, id):
        votes = VoteModel.find_by_article(id)
        if not votes:
            return {'message': f'No votes found for article with id: {id}'}, 404
        return [vote.json() for vote in votes], 200
        
    def delete(self, id):
        votes = VoteModel.find_by_article(id)
        if votes is None:
            return {'message': f'No vote found with id: {id}!'}, 404

        [vote.delete_from_db() for vote in votes]
        return {'message': f'Votes deleted for article with id: {id}!'}, 200


class VoteList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('user_id', type=str, required=True, help="Every item needs a store_id.")
    parser.add_argument('type', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('article_id', type=str, required=True, help="Every item needs a store_id.")
    
    def get(self):
        try:
            return [vote.json() for vote in VoteModel.query.all()], 200
        except:
            return {"message": "An error occurred when fetching all votes."}, 500

    def post(self):
        data = VoteList.parser.parse_args()

        try:
            vote = VoteModel(**data)
            vote.save_to_db()
        except:
            return {"message": "An error occurred inserting the vote."}, 500

        return vote.json(), 201