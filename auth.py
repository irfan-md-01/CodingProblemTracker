import bcrypt

class Auth:
    def __init__(self, db):
        self.db = db

    def register_user(self, username, password, email, phone):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if self.db.insert_user(username, hashed_password, email, phone):
            return True
        return False

    def login_user(self, username, password):
        stored_password = self.db.get_user_password(username)
        if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return True
        return False
