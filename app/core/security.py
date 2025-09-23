# core/security.py
from datetime import datetime, timedelta ,timezone ,datetime
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from core.config import settings



class SecurityManager:
  def __init__(self):
    self.secret_key=settings.SECRET_KEY
    self.algorithm=settings.ALGORITHM
    self.access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    self.refresh_token_expire_days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    self.pwd_content=CryptContext(schemes=["bcrypt"],deprecated="auto")


  def verify_password(self,plain_password:str ,hashed_password:str)->bool:
    return self.pwd_content.verify(plain_password,hashed_password)
  
  def get_password_hash(self,plain_password:str)->str:
    return self.pwd_content.hash(plain_password)
  
  def create_access_token(self,data:dict,expires_delta:Optional[timedelta]=None)->str:
    #creating JWT acceses token 
    to_encode=data.copy()  #this will copy the user ata to avoid modification 
    if expires_delta:
      expire=datetime.now(timezone.utc) + expires_delta
    else:
      expire=datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
    
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,self.secret_key,algorithm=self.algorithm)
    return encoded_jwt

  def create_refresh_token(self,data:dict)->str:
    #create Refresh jwt Token
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
    to_encode.update({})
    encode_jwt=jwt.encode(to_encode,self.secret_key,algorithm=self.algorithm)
    return encode_jwt
  
  def decode_token(self,token:str)->Dict[str , Any]:
    try:
      payload=jwt.decode(token,self.secret_key,algorithms=[self.algorithm])
      return payload
    except JWTError:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
      )
    


security_manager=SecurityManager