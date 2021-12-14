from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.comment import CommentModel

_comment_parser = reqparse.RequestParser()
_comment_parser.add_argument('date', type=str, required=False, help="Date field cannot be blank.")
_comment_parser.add_argument('author', type=str, required=False, help="Author Field cannot be blank.")
_comment_parser.add_argument('text', type=str, required=False, help="Text field cannot be blank.")
_comment_parser.add_argument('article_id', type=str, required=False, help="article_id field cannot be blank.")


class CommentByID(Resource):

    @jwt_required() # Token doesn't have to be Fresh if no arguments passed
    def get(self, id):
        comment = CommentModel.find_by_id(id)
        if not comment:
            return {'message': 'Comment not found'}, 404
        return comment.json(), 200
        
    @jwt_required() # Token doesn't have to be Fresh if no arguments passed
    def delete(self, id):
        claims = get_jwt()
        print(claims['is_admin'])
        if not claims['is_admin']:
             return {'message': 'You need Admin privileges to delete this comment.'}, 401
        comment = CommentModel.find_by_id(id)
        if comment is None:
            return {'message': f'No Comment found with id: {id}!'}, 404

        comment.delete_from_db()
        return {'message': 'Comment deleted!'}, 200

    @jwt_required()
    def put(self, id):
        data = _comment_parser.parse_args()
        comment = CommentModel.find_by_id(id)

        if not comment:
            return {'message': f'No article with title: {id} exists!'}, 404

        if 'text' in data:
            comment.text = data['text']
            
        comment.update_db()
        
        return comment.json(), 200


class CommentByAuthor(Resource):
    
    @jwt_required() # Token doesn't have to be Fresh if no arguments passed
    def get(self, author):
        comments = CommentModel.find_by_author(author)

        if not comments:
            return {'message': f'No Comments by author: {author} found!'}, 404

        return [comment.json() for comment in comments]

    @jwt_required() # Token doesn't have to be Fresh if no arguments passed
    def delete(self, author):
        comments = CommentModel.find_by_author(author)

        if len(comments) == 0:
            return {'message': f'No Comment found with author: {author}!'}, 404

        for comment in comments:
            comment.delete_from_db()
            
        return {'message': f'All comments by author: {author} deleted!'}, 200


class CommentByArticle(Resource):
    
    def get(self, article_id):
        comments = CommentModel.find_by_article(article_id)

        if not comments:
            return {'message': f'No Comments for Article with ID: {article_id} found!'}, 404

        return [comment.json() for comment in comments]
        
    @jwt_required() # Token doesn't have to be Fresh if no arguments passed
    def delete(self, article_id):
        comments = CommentModel.find_by_article(article_id)

        if len(comments) == 0:
            return {'message': f'No Comment found with ID: {article_id}!'}, 404

        for comment in comments:
            comment.delete_from_db()
            
        return {'message': f'All comments by article_id: {article_id} deleted!'}, 200


class CommentList(Resource):
    @jwt_required(optional=True) # If not logged in, user will only receive partial data with the 'optional= True' argument
    def get(self):
        user_id = get_jwt_identity()
        comments = [comment.json() for comment in CommentModel.find_all()]
        if user_id:
            return {'comments': comments}, 200

        return {
            'comments': [comment['date'] for comment in comments],
            'message': 'More data available if you log in.'
        }, 200

    def post(self):
        data = _comment_parser.parse_args()
        
        try:
            comment = CommentModel(data['date'], data['author'], data['text'], data['article_id'])
            comment.save_to_db()
        except:
            return {"message": "An error occurred inserting the comment."}, 500

        return comment.json(), 201