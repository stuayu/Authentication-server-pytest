from fastapi import APIRouter, Form , HTTPException ,Response, Request
from fastapi.responses import HTMLResponse
from functions.auth_func import *
from db.acsess import insert_registration, cur, search_username, update_pw

# routerの実装これは必須
router = APIRouter(tags=['auth'])

####### ユーザー登録
@router.post('/users/create', response_model=CreateUser)
async def regist_user(username: str = Form(...), first_pw: str = Form(...), check_pw: str = Form(...)):
    """ユーザーの登録"""
    res = search_username(cur=cur,username=username)
    if res != None:
        raise HTTPException(status_code = 400,detail="すでにそのユーザー名は使われています。別のユーザー名を登録してください。")
    check_result:bool = True
    if first_pw != check_pw:
        check_result = False
    if check_result == False:
        raise HTTPException(status_code = 400,detail="確認用パスワードと一致しません。もう一度お確かめください。")
    hash_pw = get_password_hash(first_pw)
    insert_registration(cur=cur,username=username,hashed_password=hash_pw)
    return {"results": "正常に登録できました。"}

####### パスワードの更新
@router.post('/users/update',response_model=CreateUser)
async def update_password(username: str = Form(...), old_password: str = Form(...), new_password: str = Form(...)):
    """パスワードの更新"""
    res = search_username(cur=cur,username=username)
    if res == None:
        raise HTTPException(status_code = 400,detail="ユーザーが登録されていません。")
    
    if not verify_password(old_password, res['hashed_password']):
        raise HTTPException(status_code = 400,detail="パスワードが異なります。")

    hash_pw = get_password_hash(new_password)
    update_pw(cur=cur,username=username,hashed_password=hash_pw)

    return {"results": "正常にパスワードを更新しました。"}

####### ログイン関連の実装
@router.post("/token",response_class=HTMLResponse)
async def login_for_access_token(response: Response,form_data: OAuth2PasswordRequestForm = Depends()):
    """ユーザー名とパスワードを受け取りトークンを送信する"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    #data = {"access_token": access_token, "token_type": "bearer"}
    response.set_cookie(key='token',value=access_token,httponly=True,secure=True,expires=config['token']['browser']['expires'])
    data = '''
    <!DOCTYPE html>
        <html lang="ja">
        <head>
        <meta charset="uft-8">
        <script>
        setTimeout("location.href='/'",1000*1);
        </script>
        <title>ページリダイレクト</title>
        </head>
        <body>
        <h1>リダイレクト</h1>
        <p>1秒後にジャンプします。<br>
        ジャンプしない場合は、以下のURLをクリックしてください。</p>
        <p><a href="/">移転先のページ</a></p>
        </body>
        </html>
    '''
    return data


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.get("/users/check")
async def header_ck(request: Request):
    """ヘッダーのtokenを読み取りログイン状態を確認する"""
    token = request.cookies.get('token')
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    pre_data = await get_current_user(token=token)
    current_user: User = await get_current_active_user(pre_data)
    #print(current_user)