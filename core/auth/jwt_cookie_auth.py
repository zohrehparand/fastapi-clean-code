from fastapi import Cookie, Response


def get_access_token_cookie(access_token: str | None = Cookie(default=None)):
    return access_token


def get_refresh_token_cookie(refresh_token: str | None = Cookie(default=None)):
    return refresh_token


def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )


def delete_cookies(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
