from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from models import db
from views import blacklist, UserRegisterResource, UserLoginResource, UserEditResource, UserDeleteResource, UserLogoutResource, UserViewProfileResource, BlockResource, UnblockResource, FriendshipRequestResource, FriendshipUnrequestResource, FriendshipAcceptResource, FriendshipDenyResource, FriendshipUnfriendResource, PostCreateResource, PostUpdateResource, PostDeleteResource, PostViewResource
from configparser import ConfigParser

app = Flask(__name__)
config = ConfigParser()
config.read("config.ini")

app.config["SQLALCHEMY_DATABASE_URI"] = config.get("DEFAULT", "SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_BINDS"] = {
    "password_server": config.get("DEFAULT", "SQLALCHEMY_BINDS_password_server")
}
app.config["JWT_SECRET_KEY"] = config.get("DEFAULT", "JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = config.get("DEFAULT", "JWT_TOKEN_LOCATION").split(",")

api = Api(app, prefix="/api/v1")
jwt = JWTManager(app)
db.init_app(app)

api.add_resource(UserRegisterResource, "/user/register")
api.add_resource(UserLoginResource, "/user/login")
api.add_resource(UserEditResource, "/user/edit")
api.add_resource(UserDeleteResource, "/user/delete")
api.add_resource(UserLogoutResource, "/user/logout")
api.add_resource(UserViewProfileResource, "/user/view_profile")
api.add_resource(BlockResource, "/block/block")
api.add_resource(UnblockResource, "/block/unblock")
api.add_resource(FriendshipRequestResource, "/friendship/request")
api.add_resource(FriendshipUnrequestResource, "/friendship/unrequest")
api.add_resource(FriendshipAcceptResource, "/friendship/accept")
api.add_resource(FriendshipDenyResource, "/friendship/deny")
api.add_resource(FriendshipUnfriendResource, "/friendship/unfriend")
api.add_resource(PostCreateResource, "/post/create")
api.add_resource(PostUpdateResource, "/post/update")
api.add_resource(PostDeleteResource, "/post/delete")
api.add_resource(PostViewResource, "/post/view")

if (__name__ == "__main__"):
    app.run(debug=True)
