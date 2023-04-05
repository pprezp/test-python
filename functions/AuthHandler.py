import jwt
import bcrypt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler():

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret = ''

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, hash, plain):
        return self.pwd_context.verify(plain, hash)
    
    def encode_token(self, client_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': client_id
        }

        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256']);
            return True
        except jwt.ExpiredSignatureError:
            return HTTPException(status_code=401, detail='Token Expirado')
        except jwt.InvalidTokenError:
            return HTTPException(status_code=401, detail='Token Inválido')
        
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)