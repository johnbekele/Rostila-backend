# core/security.py
from datetime import datetime, timedelta, timezone  # Fixed: removed duplicate datetime
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings


class SecurityManager:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.refresh_key = settings.REFRESH_SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, plain_password: str) -> str:
        """Hash password"""
        return self.pwd_context.hash(plain_password)

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()  # Copy user data to avoid modification
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        """Create refresh JWT token"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=self.refresh_token_expire_days
        )
        to_encode.update({"exp": expire})  # Fixed: added expiration
        encoded_jwt = jwt.encode(to_encode, self.refresh_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token and return username"""
        print(f"token: {token}")
        print(f"self.secret_key: {self.secret_key}")
        print(f"self.algorithm: {self.algorithm}")
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: Optional[str] = payload.get("sub")
            if username is None:
                return None
            return username
        except JWTError:
            return None

    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            return None

    def refresh_access_token(self, refresh_token: str) -> str:
        """Create new access token from refresh token"""
        try:
            payload = jwt.decode(
                refresh_token, self.secret_key, algorithms=[self.algorithm]
            )
            username: Optional[str] = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )

            # Create new access token
            access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
            new_token = self.create_access_token(
                data={"sub": username}, expires_delta=access_token_expires
            )
            return new_token

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

    def create_verification_token(self, user_id: str) -> str:
        """Create verification token"""
        payload = {"sub": user_id}
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        payload.update({"exp": expire})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)


# Fixed: Added parentheses to instantiate the class
security_manager = SecurityManager()
