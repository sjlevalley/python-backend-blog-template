from flask_restful import Resource, reqparse, request
import bcrypt
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Username field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="Password field cannot be blank.")
    parser.add_argument('email', type=str, required=True, help="Email field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        try: 
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
        
        except:
            return {"message": "An error occurred while creating this user."}, 500


class UserByID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=False, help="This field cannot be blank.")
    parser.add_argument('new_password', type=str, required=False, help="This field cannot be blank.")
    parser.add_argument('old_password', type=str, required=False, help="This field cannot be blank.")
    parser.add_argument('email', type=str, required=False, help="This field cannot be blank.")
    
    def get(self, id):
        try: 
            user = UserModel.find_by_id(id)
            if not user:
                return {'message': 'user not found'}, 404
            return user.json(), 200
        except:
            return {"message": "An error occurred while fetching this user."}, 500

    def delete(self, id):
        try:
            user = UserModel.find_by_id(id)

            if not user:
                return {'message': 'User does not exist!'}, 404

            user.delete_from_db()
            return {'message': 'User deleted!'}, 200
        except:
            return {"message": "An error occurred while deleting this user."}, 500

    def put(self, id):
        data = UserByID.parser.parse_args()
        user = UserModel.find_by_id(id)
        print(data)
        if not user:
                return {'message': f'No user with id: {id} exists!'}, 404

        if 'username' in data and data['username'] is not None:
            if UserModel.find_by_username(data['username']):
                return {"message": "Username Not Available"}, 400

        if 'email' in data and data['email'] is not None:
            if UserModel.find_by_username(data['email']):
                return {"message": "Email not available"}, 400
        
        if 'username' in data and (user.username != data['username']):
            user.username = data['username']

        if 'email' in data:
                user.email = data['email']

        if 'old_password' in data and 'new_password' in data:
            old_pw_encoded = data['old_password'].encode('utf-8')
            new_pw_encoded = data['new_password'].encode('utf-8')
            db_pw_encoded = user.password.encode('utf-8')
            password_valid = bcrypt.checkpw(old_pw_encoded, db_pw_encoded)
            pw_same = bcrypt.checkpw(new_pw_encoded, db_pw_encoded)

            print(password_valid)

            if not password_valid:
                return {'message': "An error occurred when trying to change password"}, 400
            
            if pw_same:
                return {'message': 'Password must be different!'}
                
            entered_password = data['new_password'].encode('utf-8')
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(entered_password, salt)
            decoded_hashed_password = hashed.decode('utf-8')

            user.password = decoded_hashed_password
            user.username = user.username
            user.email = user.email
                
            user.update_db()
        
            return user.json(), 200
         
            
            

        


class UserByUsername(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=False, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=False, help="This field cannot be blank.")
    parser.add_argument('email', type=str, required=False, help="This field cannot be blank.")
    
    def get(self, username):
        try:
            user = UserModel.find_by_username(username)
            if not user:
                return {'message': 'user not found'}, 404
            return user.json(), 200
        except:
            return {"message": "An error occurred while creating this user."}, 500

    def delete(self, username):
        try:
            user = UserModel.find_by_username(username)

            if not user:
                return {'message': 'User does not exist!'}, 404

            user.delete_from_db()
            return {'message': 'User deleted!'}, 200

        except:
            return {"message": "An error occurred while creating this user."}, 500

    def put(self, username):
        try:
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

        except:
            return {"message": "An error occurred while creating this user."}, 500


class UserList(Resource):
    def get(self):
        try:
            return list(map(lambda x: x.json(), UserModel.query.all())), 200
        except:
            return {"message": "An error occurred while creating this user."}, 500
