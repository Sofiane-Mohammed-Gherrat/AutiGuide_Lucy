# --------------------------------------------------
# Flask application configuration
# --------------------------------------------------

import os


#read the session secret key from the computer environment
#NOTE: the fallback value below is only suitable for local student-project
#demonstrations - set the AUTIGUIDE_SECRET_KEY environment variable before
#deploying this app anywhere it could be reached by the public.
SECRET_KEY = os.environ.get("AUTIGUIDE_SECRET_KEY", "student-project-secret-key")

#limit very large requests sent to the chatbot
MAX_CONTENT_LENGTH = 16384

#stop JavaScript from reading the Flask session cookie
SESSION_COOKIE_HTTPONLY = True

#add a basic cookie protection setting
SESSION_COOKIE_SAMESITE = "Lax"

#reject chat messages longer than this many characters
MAX_MESSAGE_LENGTH = 800


def apply_to(app):
    """Apply these settings to a Flask app instance."""
    app.secret_key = SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["SESSION_COOKIE_HTTPONLY"] = SESSION_COOKIE_HTTPONLY
    app.config["SESSION_COOKIE_SAMESITE"] = SESSION_COOKIE_SAMESITE
