from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt, verify_jwt_in_request
from datetime import datetime
from sqlalchemy import or_

from models import db, bcrypt, UserLogin, User, Post, Block, Friendship, PostUpdated

blacklist = set()

class UserRegisterResource(Resource):
    def post(self):
        email = request.json.get("email")
        user_name = request.json.get("user_name")
        password1 = request.json.get("password1")
        password2 = request.json.get("password2")
        parser = reqparse.RequestParser()
        parser.add_argument("public_profile", type=bool, required=False)
        parser.add_argument("country", type=str, required=False)
        parser.add_argument("biography", type=str, required=False)
        args = parser.parse_args()

        existing_email = UserLogin.query.filter_by(email=email).first()
        if existing_email:
            return {"message": "Email is already in use."}, 400
        existing_username = User.query.filter_by(user_name=user_name).first()
        if existing_username:
            return {"message": "User name is already in use."}, 400
        different_passwords = (password1 != password2)
        if different_passwords:
            return {"message": "Passwords must be the same."}, 200
        crypted_password = bcrypt.generate_password_hash(password1).decode("utf-8")

        new_userLogin = UserLogin(password=crypted_password, email=email)
        new_user = User(user_name=user_name, public_profile=args["public_profile"], country=args["country"], biography=args["biography"])
        db.session.add(new_userLogin)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.user_id)
        return {"message": "New user has successfully registered.", "access_token": access_token}, 201

class UserLoginResource(Resource):
    def post(self):
        email = request.json.get("email")
        password = request.json.get("password")

        userLogin = UserLogin.query.filter_by(email=email).first()
        if not userLogin:
            return {"message": "Invalid email."}, 400
        same_passwords = bcrypt.check_password_hash(userLogin.password, password)
        if not same_passwords:
            return {"message": "Invalid password."}, 400
        
        access_token = create_access_token(identity=userLogin.user_id)
        return {"access_token": access_token}, 200

class UserEditResource(Resource):
    @jwt_required()
    def post(self):
        email = request.json.get("email")
        user_name = request.json.get("user_name")
        password1 = request.json.get("password1")
        password2 = request.json.get("password2")
        parser = reqparse.RequestParser()
        parser.add_argument("profile_picture", type=str, required=False)
        parser.add_argument("public_profile", type=bool, required=False)
        parser.add_argument("country", type=str, required=False)
        parser.add_argument("biography", type=str, required=False)
        args = parser.parse_args()

        different_passwords = (password1 != password2)
        if (different_passwords):
            return {"message": "Passwords must be the same."}, 400
        
        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400

        email_in_use = UserLogin.query.filter_by(email=email).first()
        if email_in_use:
            if email_in_use.user_id != current_user.user_id:
                return {"message": "Email is already in use"}, 400
        
        uname_in_use = User.query.filter_by(user_name=user_name).first()
        if uname_in_use:
            if email_in_use.user_name != current_user.user_name:
                return {"message": "User name is already in use"}, 400

        current_user.user_name = user_name
        current_user.profile_picture = args["profile_picture"]
        current_user.public_profile = args["public_profile"]
        current_user.country = args["country"]
        current_user.biography = args["biography"]

        userLogin = UserLogin.query.filter_by(user_id=current_user_id).first()
        if not userLogin:
            return {"message": "Cannot find user credentials."}, 400
        userLogin.email = email
        userLogin.set_password(password1)

        db.session.commit()

        return {"message": "All information successfully updated."}, 200

class UserDeleteResource(Resource):
    @jwt_required()
    def post(self):
        email = request.json.get("email")
        password1 = request.json.get("password1")
        password2 = request.json.get("password2")
        user_id = get_jwt_identity()

        userLogin = UserLogin.query.filter_by(user_id=user_id).first()
        if not userLogin:
            return {"message": "Can not find user credentials."}, 400
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return {"message": "Can not find user."}, 400

        different_passwords = (password1 != password2)
        if (different_passwords):
            return {"message": "Passwords must be the same."}, 400

        different_email = (userLogin.email != email)
        if different_email:
            return {"message": "Invalid email address."}, 400
        
        same_passwords = bcrypt.check_password_hash(userLogin.password, password1)
        if not same_passwords:
            return {"message": "Invalid password."}, 400
        
        posts = Post.query.filter_by(user_id=user.user_id)
        if posts.first():
            for post in posts.all():
                old_post = PostUpdated.query.filter_by(post_id=post.post_id)
                if old_post.first():
                    db.session.delete(old_post.all())
            db.session.delete(posts.all())
        
        blocker = Block.query.filter_by(blocker_id=user.user_id)
        if blocker.first():
            db.session.delete(blocker.all())
        
        blocked = Block.query.filter_by(blocked_id=user.user_id)
        if blocked.first():
            db.session.delete(blocked.all())
        
        friends = Friendship.query.filter_by(user_id_1=user.user_id)
        if friends.first():
            db.session.delete(friends.all())
        friends = Friendship.query.filter_by(user_id_2=user.user_id)
        if friends.first():
            db.session.delete(friends.all())

        db.session.delete(user)
        db.session.delete(userLogin)
        db.session.commit()

        jti = get_jwt()["jti"]
        blacklist.add(jti)

        return {"message": "Successfully deleted account."}, 200

class UserViewProfileResource(Resource):
    def get(self):
        verify_jwt_in_request()
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, required=True, help="User name cannot be empty.")
        args = parser.parse_args()
        
        user = User.query.filter_by(user_name=args["user_name"]).first()
        if not user:
            return {"message": "Invalide user name"}, 400
        
        if (get_jwt_identity() != None):
            current_user_id = get_jwt_identity()
            blocked = Block.query.filter_by(blocker_id=user.user_id, blocked_id=current_user_id).first()
            if blocked:
                return {"message": "You are blocked."}, 400
        
        if user.public_profile:
            posts = Post.query.filter_by(user_id=user.user_id)
            friends = Friendship.query.filter( or_(Friendship.user_id_1==user.user_id, Friendship.user_id_2==user.user_id), Friendship.friends==True)
            pendings = Friendship.query.filter( or_(Friendship.user_id_1==user.user_id, Friendship.user_id_2==user.user_id), Friendship.friends==False)
            return {
                "country": user.country,
                "biography": user.biography,
                "joined_at": user.joined_at.isoformat(),
                "posts": [post.to_dict() for post in posts],
                "friends": [friend.to_dict() for friend in friends],
                "pending_requests": [pending.to_dict() for pending in pendings] 
            }, 200
        
        if not user.public_profile:
            id_1 = get_jwt_identity()
            id_2 = user.user_id
            if id_2 < id_1:
                id_1, id_2 = id_2, id_1
            friends = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, friends=True)
            if friends:
                posts = Post.query.filter_by(user_id=user.user_id)
                return {
                    "country": user.country,
                    "biography": user.biography,
                    "joined_at": user.joined_at.isoformat(),
                    "posts": [post.to_dict() for post in posts],
                    "friends": [friend.to_dict() for friend in friends]
                }, 200

        return {
            "country": user.country,
            "biography": user.biography,
            "joined_at": user.joined_at
        }, 200

class UserLogoutResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        blacklist.add(jti)
        return {'message': 'Successfully logged out'}, 200

class BlockResource(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, required=True, help="User name cannot be empty.")
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400

        blocked = User.query.filter_by(user_name=args["user_name"]).first()
        if not blocked:
            return {"message": "Can not find user."}, 400
        
        already_blocked = Block.query.filter_by(blocker_id=current_user.user_id, blocked_id=blocked.user_id).first()
        if already_blocked:
            return {"message": "This user is already blocked."}, 400
        
        user = User.query.filter_by(user_name=args["user_name"]).first()
        id_1 = get_jwt_identity()
        id_2 = user.user_id
        if id_2 < id_1:
            id_1, id_2 = id_2, id_1
        friends = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, friends=True).first()
        if friends:
            db.session.delete(friends)
        
        new_block = Block(blocked_id=blocked.user_id, blocker_id=current_user.user_id)
        db.session.add(new_block)
        db.session.commit()
        return {"message": "Successfully blocked user."}, 200

class UnblockResource(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, required=True, help="User name cannot be empty.")
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400

        blocked = User.query.filter_by(user_name=args["user_name"]).first()
        if not blocked:
            return {"message": "Can not find user."}, 400
        
        block = Block.query.filter_by(blocker_id=current_user.user_id, blocked_id=blocked.user_id).first()
        if not block:
            return {"message": "This user is not blocked."}, 400
        
        db.session.delete(block)
        db.session.commit()
        return {"message": "Successfully unblocked user."}, 200

class FriendshipRequestResource(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, required=True, help="User name cannot be empty.")
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400
        
        user = User.query.filter_by(user_name=args["user_name"]).first()
        if not user:
            return {"message": "Cannot find user."}, 400
        
        blocked = Block.query.filter_by(blocker_id=user.user_id, blocked_id=current_user.user_id).first()
        if blocked:
            return {"message": "You are blocked by this user."}, 400
        blocker = Block.query.filter_by(blocker_id=current_user.user_id, blocked_id=user.user_id).first()
        if blocker:
            return {"message": "You have blocked this user."}, 400
        
        id_1 = current_user.user_id
        id_2 = user.user_id
        if id_2 < id_1:
            id_1, id_2 = id_2, id_1
        friendship_request_send = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, friends=False).first()
        if friendship_request_send:
            if friendship_request_send.request_from == current_user_id:
                return {"message": "You have already sent a friendship request to this user."}, 400
            else:
                return {"message": "This user has already sent a friendship request to you."}, 400
        already_friends = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, friends=True).first()
        if already_friends:
            return {"message": "You are already friends with this user."}, 400
        
        friendship_request = Friendship(user_id_1=id_1, user_id_2=id_2, request_from=current_user.user_id)
        db.session.add(friendship_request)
        db.session.commit()
        return {"message": "Successfully sent friendship request."}, 200

class FriendshipUnrequestResource(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, required=True, help="User name cannot be empty.")
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400
        
        user = User.query.filter_by(user_name=args["user_name"]).first()
        if not user:
            return {"message": "Cannot find user."}, 400
        
        blocked = Block.query.filter_by(blocker_id=user.user_id, blocked_id=current_user.user_id).first()
        if blocked:
            return {"message": "You are blocked by this user."}, 400
        blocker = Block.query.filter_by(blocker_id=current_user.user_id, blocked_id=user.user_id).first()
        if blocker:
            return {"message": "You have blocked this user."}, 400
        
        id_1 = current_user.user_id
        id_2 = user.user_id
        if id_2 < id_1:
            id_1, id_2 = id_2, id_1
        already_friends = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, friends=True).first()
        if already_friends:
            return {"message": "You are already friends with this user."}, 400
        friendship_request_send = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, request_from=current_user.user_id, friends=False).first()
        if not friendship_request_send:
            return {"message": "There is no friendship request sent to this user."}, 400
        friendship_request_received = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, request_from=user.user_id, friends=False).first()
        if friendship_request_received:
            return {"message": "There is no friendship request sent to this user."}, 400
        
        db.session.delete(friendship_request_send)
        db.session.commit()
        return {"message": "Successfully unsent friendship request."}, 200

class FriendshipAcceptResource(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, required=True, help="User name cannot be empty.")
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400
        
        user = User.query.filter_by(user_name=args["user_name"]).first()
        if not user:
            return {"message": "Cannot find user."}, 400
        
        blocked = Block.query.filter_by(blocker_id=user.user_id, blocked_id=current_user.user_id).first()
        if blocked:
            return {"message": "You are blocked by this user."}, 400
        blocker = Block.query.filter_by(blocker_id=current_user.user_id, blocked_id=user.user_id).first()
        if blocker:
            return {"message": "You have blocked this user."}, 400
        
        id_1 = current_user.user_id
        id_2 = user.user_id
        if id_2 < id_1:
            id_1, id_2 = id_2, id_1
        already_friends = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, friends=True).first()
        if already_friends:
            return {"message": "You are already friends with this user."}, 400
        friendship_request_send = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, request_from=user.user_id, friends=False).first()
        if not friendship_request_send:
            return {"message": "There is no friendship request from this user."}, 400
        
        friendship_request_send.friends = True
        friendship_request_send.started_at = datetime.now()
        db.session.commit()
        return {"message": "Successfully accepted friendship request."}, 200

class FriendshipDenyResource(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, required=True, help="User name cannot be empty.")
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400
        
        user = User.query.filter_by(user_name=args["user_name"]).first()
        if not user:
            return {"message": "Cannot find user."}, 400
        
        blocked = Block.query.filter_by(blocker_id=user.user_id, blocked_id=current_user.user_id).first()
        if blocked:
            return {"message": "You are blocked by this user."}, 400
        blocker = Block.query.filter_by(blocker_id=current_user.user_id, blocked_id=user.user_id).first()
        if blocker:
            return {"message": "You have blocked this user."}, 400
        
        id_1 = current_user.user_id
        id_2 = user.user_id
        if id_2 < id_1:
            id_1, id_2 = id_2, id_1
        already_friends = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, friends=True).first()
        if already_friends:
            return {"message": "You are already friends with this user."}, 400
        friendship_request_send = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, request_from=user.user_id, friends=False).first()
        if not friendship_request_send:
            return {"message": "There is no friendship request from this user."}, 400
        
        db.session.delete(friendship_request_send)
        db.session.commit()
        return {"message": "Successfully denied friendship request."}, 200

class FriendshipUnfriendResource(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, required=True, help="User name cannot be empty.")
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400
        
        user = User.query.filter_by(user_name=args["user_name"]).first()
        if not user:
            return {"message": "Cannot find user."}, 400
        
        blocked = Block.query.filter_by(blocker_id=user.user_id, blocked_id=current_user.user_id).first()
        if blocked:
            return {"message": "You are blocked by this user."}, 400
        blocker = Block.query.filter_by(blocker_id=current_user.user_id, blocked_id=user.user_id).first()
        if blocker:
            return {"message": "You have blocked this user."}, 400
        
        id_1 = current_user.user_id
        id_2 = user.user_id
        if id_2 < id_1:
            id_1, id_2 = id_2, id_1
        friendship = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, friends=True).first()
        if not friendship:
            return {"message": "You are not friends with this user."}, 400
        
        db.session.delete(friendship)
        db.session.commit()
        return {"message": "Successfully unfriended this user."}, 200

class PostCreateResource(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text", type=str, required=True, help="Text cannot be empty")
        parser.add_argument("photo", type=str, required=False)
        parser.add_argument("video", type=str, required=False)
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400
        
        new_post = Post(user_id=current_user.user_id, text=args["text"])
        db.session.add(new_post)
        db.session.commit()
        return {"message": "Successfully created post."}, 200

class PostUpdateResource(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("post_id", type=str, required=True, help="Post id cannot be empty")
        parser.add_argument("text", type=str, required=True, help="Text cannot be empty")
        parser.add_argument("photo", type=str, required=False)
        parser.add_argument("video", type=str, required=False)
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400
        
        post = Post.query.filter_by(post_id=args["post_id"]).first()
        if not post:
            return {"message": "Can not find post."}, 400
        
        old_post = PostUpdated(post_id=args["post_id"], old_text=post.text, old_photo=post.photo, old_video=post.video)
        post.text = args["text"]
        post.edited = True
        post.edited_at = datetime.now()

        db.session.add(old_post)
        db.session.commit()
        return {"message": "Successfully updated post."}, 200

class PostDeleteResource(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("post_id", type=str, required=True, help="Post id cannot be empty")
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400
        
        post = Post.query.filter_by(post_id=args["post_id"]).first()
        if not post:
            return {"message": "Can not find post."}, 400
        
        old_posts = PostUpdated.query.filter_by(post_id=args["post_id"]).all()
        if post.edited and old_posts:
            for old_post in old_posts:
                db.session.delete(old_post)

        db.session.delete(post)
        db.session.commit()
        return {"message": "Successfully deleted post."}, 200

class PostViewResource(Resource):
    def get(self):
        verify_jwt_in_request()
        parser = reqparse.RequestParser()
        parser.add_argument("post_id", type=str, required=True, help="Post id cannot be empty")
        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        if (current_user_id != None):
            current_user = User.query.filter_by(user_id=current_user_id).first()
            if not current_user:
                return {"message": "Invalid access token"}, 400
        
        post = Post.query.filter_by(post_id=args["post_id"]).first()
        if not post:
            return {"message": "Can not find post."}, 400
        
        user_id = post.user_id
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return {"message": "Can not find the original poster."}, 400
        public_profile = user.public_profile
        if public_profile:
            data = {
                "user_name": user.user_name,
                "post_id": post.post_id,
                "text": post.text,
                "photo": post.photo,
                "video": post.video,
                "edited": post.edited,
                "created_at": post.created_at.isoformat(),
            }
            if post.edited:
                data["edited_at"] = post.edited_at.isoformat()
            return data, 200
        
        current_user_id = get_jwt_identity()
        if (current_user_id == None):
            return {"message": "This post is private."}, 400
    
        current_user = User.query.filter_by(user_id=current_user_id).first()
        if not current_user:
            return {"message": "Invalid access token"}, 400
        
        blocked = Block.query.filter_by(blocker_id=user.user_id, blocked_id=current_user.user_id).first()
        if blocked:
            return {"message": "You are blocked by this user."}, 400
        blocker = Block.query.filter_by(blocker_id=current_user.user_id, blocked_id=user.user_id).first()
        if blocker:
            return {"message": "You have blocked this user."}, 400
        
        id_1 = current_user.user_id
        id_2 = user.user_id
        if id_2 < id_1:
            id_1, id_2 = id_2, id_1
        friends = Friendship.query.filter_by(user_id_1=id_1, user_id_2=id_2, friends=True).first()
        if not friends:  
            return {
                "user_name": user.user_name,
                "post_id": post.post_id,
                "text": post.text,
                "photo": post.photo,
                "video": post.video,
                "edited": post.edited,
                "created_at": post.created_at.isoformat(),
                "edited_at": post.edited_at.isoformat()
            }, 200
        
        return {"message": "This post is private."}, 400
        
