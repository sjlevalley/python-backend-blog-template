from flask_restful import Resource, request, reqparse
from sqlalchemy import update
from models.article import ArticleModel



class Article(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=False, help="Title cannot be blank.")
    parser.add_argument('subtitle', type=str, required=False, help="Subtitle cannot be blank.")
    parser.add_argument('date', type=str, required=False, help="Date field cannot be blank.")
    parser.add_argument('author', type=str, required=False, help="Author field cannot be blank.")
    parser.add_argument('text', type=str, required=False, help="Text field cannot be blank.")
    
    def get(self, title):
        try: 
            article = ArticleModel.find_by_title(title)
        except:
            return {"message": "An error occurred while trying to find this article."}, 500

        if not article:
            return {'message': 'Article not found'}, 404

        return article.json(), 200

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

    def put(self, title):
        data = Article.parser.parse_args()
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
        

class ArticleList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="Title cannot be blank.")
    parser.add_argument('subtitle', type=str, required=True, help="Subtitle cannot be blank.")
    parser.add_argument('date', type=str, required=True, help="Date field cannot be blank.")
    parser.add_argument('author', type=str, required=True, help="Author field cannot be blank.")
    parser.add_argument('text', type=str, required=True, help="Text field cannot be blank.")

    def get(self):
        try:
            return [article.json() for article in ArticleModel.query.all()]
        except:
            return {"message": "An error occurred while trying to fetch all articles."}, 500

    def post(self):
        data = ArticleList.parser.parse_args()
        
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