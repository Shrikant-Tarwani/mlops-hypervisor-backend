from passlib.context import CryptContext
import jwt
import datetime
from src.db.models import Organization, User
from src.db.database import get_db
from sqlalchemy.orm import Session

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = "your_secret_key"  # Replace with a secure key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: datetime.timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def register_user(self, username: str, password: str, invite_code: str):
        # Logic to register a user, validate invite code, and save to the database
        organization = self.db.query(Organization).filter_by(invite_code=invite_code).first()
        if not organization:
            return False
        hashed_password = self.hash_password(password)
        new_user = User(username=username, password_hash=hashed_password, organization_id=organization.id)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def authenticate_user(self, username: str, password: str):
        user = self.db.query(User).filter(User.username == username).first()
        if user and self.verify_password(password, user.password):
            return user
        return None

    def get_current_user(self, token: str):
        credentials_exception = Exception("Could not validate credentials")
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except jwt.PyJWTError:
            raise credentials_exception
        return username