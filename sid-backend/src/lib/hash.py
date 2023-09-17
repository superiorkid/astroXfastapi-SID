from passlib.context import CryptContext


class Hash:
    password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.password_ctx.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.password_ctx.verify(plain_password, hashed_password)
