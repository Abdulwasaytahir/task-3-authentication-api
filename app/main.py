from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from .database import (
    engine,
    Base,
    get_db
)

from .models import User

from .schemas import (
    UserCreate,
    UserResponse,
    TokenResponse
)

from .crud import (
    create_user,
    get_user_by_email,
    verify_password
)

from .auth import (
    create_access_token,
    verify_token
)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Authentication API"
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


@app.get("/")
def home():

    return {
        "message": "Authentication API is running"
    }


@app.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return create_user(
        db,
        user
    )


@app.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = get_user_by_email(
        db,
        form_data.username
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    password_correct = verify_password(
        form_data.password,
        db_user.password_hash
    )

    if not password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_access_token(
        data={
            "sub": str(db_user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = verify_token(token)

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    user_id = payload.get("sub")

    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    try:
        user_id = int(user_id)

    except ValueError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    current_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if current_user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return current_user


@app.get(
    "/protected",
    response_model=UserResponse
)
def protected_route(
    current_user: User = Depends(get_current_user)
):

    return current_user