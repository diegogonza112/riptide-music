from flask_sqlalchemy import SQLAlchemy

import generate_user

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username):
        if username == "guest.user.buddy":
            self.username = generate_user.generate_user()
        else:
            self.username = username

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def get_pseudonym(self):

        return self.pseudonym

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def __repr__(self):
        return f"{self.get_id()}"
