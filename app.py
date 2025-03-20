from flask import Flask
from config import Config
from extensions import db, migrate, admin
from routes.__init__ import routes



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)
routes(app)


if __name__ == "__main__":
    app.run(debug=True)
