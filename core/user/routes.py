from fastapi import APIRouter, Depends, HTTPException, status,Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.app.database import get_db
from core.auth.jwtauth import decode_refresh_token, generate_access_token, generate_refresh_token
from core.auth.security import hash_password, verify_password
from core.user.model import UserModel
from core.user.schema import UserRefreshTokenSchema, UserRegisterSchema
from core.auth.jwt_cookie_auth import set_auth_cookies,delete_cookies

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    username = request.username.strip().lower()

    if db.query(UserModel).filter(UserModel.username == username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    user = UserModel(username=username, password=hash_password(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"detail": "User registered successfully"}


@router.post("/login")
def login(response: Response,form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username.strip().lower()).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token= generate_access_token(user.id)
    refresh_token= generate_refresh_token(user.id)
    set_auth_cookies(response,access_token,refresh_token)    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }    

@router.post("/refresh-token")
def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )

    user_id = decode_refresh_token(refresh_token)

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    access_token = generate_access_token(user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return {
        "message": "Access token refreshed",
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(response: Response):
    delete_cookies(response)

    return {
        "message": "Logout successful"
    }