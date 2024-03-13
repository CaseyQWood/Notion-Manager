import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

## Initialize database
Base = declarative_base()
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    conversation = Column(JSONB)

    ## Add message to database


def add_user(name):
    """Add user to database."""
    new_user = User(name=name)
    with Session() as session:
        session.add(new_user)
        session.commit()


def update_user(user_id, name):
    """Update user in database."""
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        user.name = name
        session.commit()


def get_user(user_id):
    """Get user from database."""
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        return user


def add_conversation(user_id, conversation):
    """Add conversation to database."""
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        user.conversation = conversation
        session.commit()


def update_conversation(user_id, conversation):
    """Update conversation in database."""
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        user.conversation = conversation
        session.commit()


def get_conversation(user_id):
    """Get conversation from database."""
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        return user.conversation


def get_user_id(name):
    with Session() as session:
        user = session.query(User).filter(User.name == name).first()
        return user.id


Base.metadata.create_all(engine)
