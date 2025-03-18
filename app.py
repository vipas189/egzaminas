from flask import Flask
from config import Config
from extensions import db, migrate
from routes.__init__ import routes
from models.users import Users


def main():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    routes(app)

    app.run(debug=True)


if __name__ == "__main__":
    main()
