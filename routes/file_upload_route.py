import os
from flask import request, redirect, url_for, flash
import uuid
from flask_login import current_user
from extensions import db
from flask_login import login_required
from services.file_upload_services import allowed_file


def file_upload_route(app):
    @app.route("/upload", methods=["POST"])
    @login_required
    def upload_file():
        if "file" not in request.files:
            return redirect(url_for(f"panel_{current_user.role}"))
        file = request.files["file"]
        valid = allowed_file(file)
        if not valid:
            flash("Perdidele nuotrauka", category="picture_error")
            return redirect(url_for(f"panel_{current_user.role}"))
        file.seek(0)
        filename = str(uuid.uuid4()) + "_" + file.filename
        file.save(os.path.join("static/uploads", filename))
        current_user.profile_picture = f"uploads/{filename}"
        db.session.commit()
        return redirect(url_for(f"panel_{current_user.role}"))
