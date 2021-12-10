from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.comment import CommentModel


class CommentByID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date', type=str, required=False, help="Date field cannot be blank.")
    parser.add_argument('author', type=str, required=False, help="Author Field cannot be blank.")
    parser.add_argument('text', type=str, required=False, help="Text field cannot be blank.")
    parser.add_argument('article_id', type=str, required=False, help="article_id field cannot be blank.")

    # @jwt_required()
    def get(self, id):
        comment = CommentModel.find_by_id(id)
        if not comment:
            return {'message': 'Comment not found'}, 404
        return comment.json(), 200
        
    def delete(self, id):
        comment = CommentModel.find_by_id(id)
        if comment is None:
            return {'message': f'No Comment found with id: {id}!'}, 404

        comment.delete_from_db()
        return {'message': 'Comment deleted!'}, 200

    def put(self, id):
        data = CommentByID.parser.parse_args()
        comment = CommentModel.find_by_id(id)

        if not comment:
            return {'message': f'No article with title: {id} exists!'}, 404

        if 'text' in data:
            comment.text = data['text']
            
        comment.update_db()
        
        return comment.json(), 200

class CommentByAuthor(Resource):
    
    # @jwt_required()
    def get(self, author):
        comments = CommentModel.find_by_author(author)

        if not comments:
            return {'message': f'No Comments by author: {author} found!'}, 404

        return [comment.json() for comment in comments]
        
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
        
    def delete(self, article_id):
        comments = CommentModel.find_by_article(article_id)

        if len(comments) == 0:
            return {'message': f'No Comment found with ID: {article_id}!'}, 404

        for comment in comments:
            comment.delete_from_db()
            
        return {'message': f'All comments by article_id: {article_id} deleted!'}, 200


class CommentList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date', type=str, required=True, help="Date field cannot be blank.")
    parser.add_argument('author', type=str, required=True, help="Author Field cannot be blank.")
    parser.add_argument('text', type=str, required=True, help="Text field cannot be blank.")
    parser.add_argument('article_id', type=str, required=True, help="article_id field cannot be blank.")
    
    def get(self):
        return list(map(lambda x: x.json(), CommentModel.query.all())), 200

    def post(self):
        data = CommentList.parser.parse_args()
        
        try:
            comment = CommentModel(**data)
            comment.save_to_db()
        except:
            return {"message": "An error occurred inserting the comment."}, 500

        return comment.json(), 201