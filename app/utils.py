from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hahsing_password(text_password:str):
    hash_password = pwd_context.hash(text_password)
    return hash_password

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)