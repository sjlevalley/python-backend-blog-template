from flask_restful import Resource, reqparse, request
import bcrypt
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('email', type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        if UserModel.find_by_username(data['email']):
            return {"message": "A user with that email already exists"}, 400

        entered_password = data['password'].encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(entered_password, salt)
        decoded_hashed_password = hashed.decode('utf-8')
        
        user = UserModel(data['username'], decoded_hashed_password, data['email'])
        user.save_to_db()

        return user.json() , 201


class UserByID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=False, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=False, help="This field cannot be blank.")
    parser.add_argument('email', type=str, required=False, help="This field cannot be blank.")
    
    def get(self, id):
        user = UserModel.find_by_id(id)
        if not user:
            return {'message': 'user not found'}, 404
        return user.json(), 200

    def delete(self, id):
        user = UserModel.find_by_id(id)

        if not user:
            return {'message': 'User does not exist!'}, 404

        user.delete_from_db()
        return {'message': 'User deleted!'}, 200

    def put(self, id):
        data = UserByID.parser.parse_args()
        user = UserModel.find_by_id(id)
        
        if not user:
            return {'message': f'No user with id: {id} exists!'}, 404

        if 'username' in data:
            if UserModel.find_by_username(data['username']):
                return {"message": "Username Not Available"}, 400

        if 'email' in data:
            if UserModel.find_by_username(data['email']):
                return {"message": "Please use a different email"}, 400
    
        if 'username' in data and (user.username != data['username']):
            user.username = data['username']

        if 'email' in data:
            user.email = data['email']
            
        user.update_db()
        
        return user.json(), 200


class UserByUsername(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=False, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=False, help="This field cannot be blank.")
    parser.add_argument('email', type=str, required=False, help="This field cannot be blank.")
    
    def get(self, username):
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': 'user not found'}, 404
        return user.json(), 200

    def delete(self, username):
        user = UserModel.find_by_username(username)

        if not user:
            return {'message': 'User does not exist!'}, 404

        user.delete_from_db()
        return {'message': 'User deleted!'}, 200

    def put(self, username):
        data = UserByUsername.parser.parse_args()

        user = UserModel.find_by_username(username)
        if not user:
            return {'message': f'No user with username: {username} exists!'}, 404

        data = request.get_json()

        if 'username' in data:
            if UserModel.find_by_username(data['username']):
                return {"message": "Username not available, please select a unique username"}, 400

        if 'email' in data:
            if UserModel.find_by_username(data['email']):
                return {"message": "Please use a different email"}, 400
    
        if 'username' in data and (user.username != data['username']):
            user.username = data['username']

        if 'email' in data:
            user.email = data['email']
            
        user.update_db()
        
        return user.json(), 200


class UserList(Resource):
    
    def get(self):
        return list(map(lambda x: x.json(), UserModel.query.all())), 200
