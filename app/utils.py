
from passlib.context import CryptContext

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password):
   return pwd_context.hash(password)

def verify_pass(user_password, database_password ):
   return pwd_context.verify(user_password, database_password)