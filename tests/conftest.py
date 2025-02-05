import datetime
import logging
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.auth.service import create_refresh_token, create_token_set, save_refresh_token
from src.database.core import Base

from src.applications.models import Application, Rating
from src.auth.models import RefreshToken
from src.enums import AccountType
from src.users.models import User
from src.comments.models import Comment, CommentVotes
from src.reviews.models import Review, ReviewVotes
from src.main import app
from src.dependencies import get_db
from src import pwd_context, config


SQLALCHEMY_DATABASE_URI =  "sqlite:///test.db"



@pytest.fixture(scope="module")
def database_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})

    Base.metadata.create_all(bind=engine)  
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def session(database_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False)
    session = SessionLocal(bind=database_engine)
    yield session
    
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def client(session):
    def overrided_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrided_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def access_token(session, user):
    token_set = create_token_set(session, user, scopes=["users", "applications", "me"])
    return token_set.access_token


@pytest.fixture(scope="function")
def client_with_auth(session, access_token: str, refresh_token):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        test_client.headers.update({"Authorization": f"Bearer {access_token}"})
        test_client.cookies.update(cookies={"refresh_token": refresh_token})
        yield test_client

    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="function")
def user(session):
    user = session.query(User).filter_by(username="testusername").first()
    if not user:
        user = User(email="testemail@gmail.com", username="testusername", password=pwd_context.hash("testpassword"), account_type=AccountType.tester.value)
        session.add(user)
    session.commit()
    yield user


@pytest.fixture
def application(session, user: User):
    app = session.query(Application).filter_by(name="Test App").first()
    if not app:
        app = Application(name="Test App", description="stringstringstringstringstringstringstringstringklklkklklstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringst", user_id=user.id, hide_reviews=False)
        session.add(app)
        session.commit()
    return app


@pytest.fixture(scope="function")
def refresh_token(session, user):
    refresh_token = create_refresh_token(
        dict(token_type=config.REFRESH_TOKEN_TYPE, user_id=user.id, scopes="applications users me")
    )
    save_refresh_token(session, refresh_token, user, datetime.timedelta(config.REFRESH_TOKEN_EXPIRE_DAYS))
    yield refresh_token


@pytest.fixture(scope="function")
def review(session, user, application):
    review = session.query(Review).filter_by(title="title", body="body", user_id=user.id).first()
    if not review:
        review = Review(title="title", body="body", user_id=user.id)
        session.add(review)
        session.commit()
    return review


@pytest.fixture(scope="function")
def comment(session, user, review):
    comment = session.query(Comment).filter_by(text="text", review_id=review.id, user_id=user.id).first()
    if not comment:
        comment = Comment(text="text", review_id=review.id, user_id=user.id)
        session.add(comment)
        session.commit()
    return comment
