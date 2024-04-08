from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = "cosmocrew.db"

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
session = sessionmaker(bind=engine)

base = declarative_base()


def create_db():
    base.metadata.create_all(engine)