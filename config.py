class APIConfig:
    API_TITLE = "Eco Echo API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_UI_URL = "https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@hostname/eco_echo'