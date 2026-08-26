from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.app.database import get_db
from core.auth.jwtauth import (
    decode_refresh_token,
    generate_access_token,
    generate_refresh_token,
)
from core.auth.security import hash_password, verify_password
from core.user.model import UserModel
from core.user.schema import UserRegisterSchema
from core.auth.jwt_cookie_auth import set_auth_cookies, delete_cookies
from core.app.language import get_language
from core.app.translator import translate

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def user_register(
    request: UserRegisterSchema,
    db: Session = Depends(get_db),
    language: str = Depends(get_language),
):
    username = request.username.strip().lower()

    if db.query(UserModel).filter(UserModel.username == username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=translate("username_exists", language),
        )

    user = UserModel(username=username, password=hash_password(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"detail": translate("user_registered", language)}


@router.post("/login")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    language: str = Depends(get_language),
):
    user = (
        db.query(UserModel)
        .filter(UserModel.username == form_data.username.strip().lower())
        .first()
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate("incorrect_credentials", language),
        )
    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)
    set_auth_cookies(response, access_token, refresh_token)
    return {
        "message": translate("login_successful", language),
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token")
def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
    language: str = Depends(get_language),
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate("refresh_token_not_found", language),
        )

    user_id = decode_refresh_token(refresh_token)

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate("user_not_found", language),
        )

    access_token = generate_access_token(user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return {
        "message": translate("access_token_refreshed", language),
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(response: Response, language: str = Depends(get_language)):
    delete_cookies(response)

    return {"message": translate("logout_successful", language)}
