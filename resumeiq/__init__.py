"""Flask application factory. Business logic lives outside HTTP routes."""
import os
import secrets
from pathlib import Path

from flask import Flask, flash, redirect, url_for

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder=str(PROJECT_ROOT / "templates"),
        static_folder=str(PROJECT_ROOT / "public" / "static"),
        static_url_path="/static",
    )
    app.config.update(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32),
        MAX_CONTENT_LENGTH=4 * 1024 * 1024,
        MAX_UPLOAD_FILES=5,
        MAX_FILE_BYTES=3 * 1024 * 1024,
        MAX_JOB_DESCRIPTION_CHARS=5000,
    )
    if test_config:
        app.config.update(test_config)

    from resumeiq.routes import screening
    app.register_blueprint(screening)

    @app.errorhandler(413)
    def oversized_request(_error):
        flash("Upload too large. Keep all files and form data under 4 MB.", "error")
        return redirect(url_for("screening.index")), 303

    return app
