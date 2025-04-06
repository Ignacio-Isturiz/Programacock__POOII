class User:
    def __init__(self, id, username, email, password_hash, is_active=False, recovery_token=None, token_expiration=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active
        self.recovery_token = recovery_token
        self.token_expiration = token_expiration

    def __repr__(self):
        return f"<User {self.username}>"
