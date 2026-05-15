from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DBModelBase

DATABASE_URL = "sqlite:///healthtrack_clinic.sqlite"

engine = create_engine(DATABASE_URL)
DBModelBase.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)