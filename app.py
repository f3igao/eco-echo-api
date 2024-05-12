from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from db import db
from resources.activity import blp as ActivityBluePrint
from resources.activity_review import blp as ActivityReviewBluePrint
from resources.park import blp as ParkBluePrint
from resources.park_review import blp as ParkReviewBlueprint
from resources.state import blp as StateBlueprint
from resources.user import blp as UserBlueprint
from resources.user_activity_review import blp as UserActivityReviewBlueprint
from resources.user_activity_tag import blp as UserActivityTagBlueprint


class APIConfig:
    API_TITLE = "Eco Echo API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_UI_URL = "https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost/eco_echo"


app = Flask(__name__)
app.config.from_object(APIConfig)

cors = CORS(app, origins="http://localhost:5173")

db.init_app(app)
api = Api(app)

api.register_blueprint(ActivityBluePrint)
api.register_blueprint(ActivityReviewBluePrint)
api.register_blueprint(ParkBluePrint)
api.register_blueprint(ParkReviewBlueprint)
api.register_blueprint(StateBlueprint)
api.register_blueprint(UserBlueprint)
api.register_blueprint(UserActivityReviewBlueprint)
api.register_blueprint(UserActivityTagBlueprint)
