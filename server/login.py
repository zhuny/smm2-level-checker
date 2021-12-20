from flask import Flask
from flask_login import LoginManager


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def is_anonymous(self):
        return False


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


def init(app: Flask):
    login_manager.init_app(app)
    if app.debug:
        from flask_login import AnonymousUserMixin

        class SuperUser(AnonymousUserMixin):
            def __init__(self):
                self.user_id = 83

        login_manager.anonymous_user = SuperUser
