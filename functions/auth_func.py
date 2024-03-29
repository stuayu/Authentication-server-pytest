from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.auth_m import *
from db.acsess import cur, search_username
import yaml

with open('config.yml', encoding='utf8') as file:
    config = yaml.safe_load(file.read())

# to get a string like this run:
# JWTトークンの署名に使用されるランダムな秘密鍵を生成(以下の鍵は例)
# openssl rand -hex 32
SECRET_KEY = config['token']['backend']['SECRET_KEY']
# JWTトークンの署名に使用するアルゴリズム
ALGORITHM = config['token']['backend']['ALGORITHM']
# トークンの有効期限(min)
ACCESS_TOKEN_EXPIRE_MINUTES = config['token']['backend']['expires']
# トークンの有効期限(min)
ACCESS_TOKEN_EXPIRE_MINUTES_REFLESH = config['token']['backend']['refresh']

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)




def get_password_hash(password):

    return pwd_context.hash(password)

def get_user(username: str):
    db = search_username(cur,username)
    #print(db)
    try:
        if username in db['username']:
            user_dict = db
            return UserInDB(**user_dict)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail='ユーザー名が存在しません再度確認してください。'
        )


def authenticate_user(username: str, password: str):

    user = get_user(username)

    if not user:

        return False

    if not verify_password(password, user.hashed_password):

        return False

    return user



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    #print(current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
