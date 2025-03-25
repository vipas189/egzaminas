import os
from flask import request, redirect, url_for
import uuid
from flask_login import current_user
from extensions import db


def file_upload_route(app):
    @app.route("/upload", methods=["POST"])
    def upload_file():
        # if "file" not in request.files:
        #     return "No file uploaded", 400

        file = request.files["file"]
        filename = str(uuid.uuid4()) + "_" + file.filename
        file.save(os.path.join("static/uploads", filename))
        current_user.profile_picture = url_for("static", filename=f"uploads/{filename}")
        db.session.commit()
        return redirect(url_for("panel_student"))

        # if file.filename == "":
        #     return "No selected file", 400

        # return "File uploaded successfully", 200
