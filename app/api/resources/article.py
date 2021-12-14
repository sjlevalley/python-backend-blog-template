from flask_restful import Resource, request, reqparse
from sqlalchemy import update
from flask_jwt_extended import jwt_required
from models.article import ArticleModel


_article_parser = reqparse.RequestParser()
_article_parser.add_argument('title', type=str, required=False, help="Title cannot be blank.")
_article_parser.add_argument('subtitle', type=str, required=False, help="Subtitle cannot be blank.")
_article_parser.add_argument('date', type=str, required=False, help="Date field cannot be blank.")
_article_parser.add_argument('author', type=str, required=False, help="Author field cannot be blank.")
_article_parser.add_argument('text', type=str, required=False, help="Text field cannot be blank.")

class ArticleByTitle(Resource):
    
    def get(self, title): 
        try: 
            article = ArticleModel.find_by_title(title)
        except:
            return {"message": "An error occurred while trying to find this article."}, 500

        if not article:
            return {'message': 'Article not found'}, 404

        return article.json(), 200

    # @jwt_required() # Token doesn't have to be Fresh if no arguments passed
    def delete(self, title):
        try: 
            article = ArticleModel.find_by_title(title)
        except:
            return {"message": "An error occurred while trying to find this article."}, 500


        if not article:
            return {'message': 'Article does not exist!'}, 404

        try:
            article.delete_from_db()
            return {'message': 'Article deleted!'}, 200
        except:
            return {"message": "An error occurred while trying to delete this article."}, 500

    # @jwt_required()
    def put(self, title): # Currently set up to only be able to edit the text
        data = _article_parser.parse_args()
        try: 
            article = ArticleModel.find_by_title(title)
        except:
            return {"message": "An error occurred while trying to find this article."}, 500

        if not article:
            return {'message': f'No article with title: {title} exists!'}, 404

        if 'text' in data and (article.text != data['text']):
            article.text = data['text']
            
        try:
            article.update_db()
            return {'message': 'Article updated!'}, 200
        except:
            return {"message": "An error occurred while trying to update this article."}, 500


class ArticleByID(Resource):
    
    def get(self, id):
        try: 
            article = ArticleModel.find_by_id(id)
        except:
            return {"message": "An error occurred while trying to find this article."}, 500

        if not article:
            return {'message': 'Article not found'}, 404

        return article.json(), 200

    # @jwt_required() # Token doesn't have to be Fresh if no arguments passed
    def delete(self, id):
        try: 
            article = ArticleModel.find_by_id(id)
        except:
            return {"message": "An error occurred while trying to find this article."}, 500


        if not article:
            return {'message': 'Article does not exist!'}, 404

        try:
            article.delete_from_db()
            return {'message': 'Article deleted!'}, 200
        except:
            return {"message": "An error occurred while trying to delete this article."}, 500

    # @jwt_required() # Token doesn't have to be Fresh if no arguments passed
    def put(self, id): # Currently set up to only be able to edit the text
        data = _article_parser.parse_args()
        try: 
            article = ArticleModel.find_by_id(id)
        except:
            return {"message": "An error occurred while trying to find this article."}, 500

        if not article:
            return {'message': f'No article with title: {id} exists!'}, 404

        if 'text' in data and (article.text != data['text']):
            article.text = data['text']
            
        try:
            article.update_db()
            return {'message': 'Article updated!'}, 200
        except:
            return {"message": "An error occurred while trying to update this article."}, 500
        

class ArticleList(Resource):

    def get(self):
        try:
            return [article.json() for article in ArticleModel.find_all()]
        except:
            return {"message": "An error occurred while trying to fetch all articles."}, 500

    def post(self):
        data = _article_parser.parse_args()
        
        try:
            existing_article = ArticleModel.find_by_title(data['title'])
        except:
            return {"message": "An error occurred while trying to find this article."}, 500
        

        if existing_article:
            return {'message': "An Article with title '{}' already exists.".format(data['title'])}, 400

        article = ArticleModel(**data)

        try:
            article.save_to_db()
        except:
            return {"message": "An error occurred creating the article."}, 500

        return article.json(), 201