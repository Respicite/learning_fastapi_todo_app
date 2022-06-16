import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_string = os.environ.get('DATABASE_URL_PG')
# db_string = 'postgresql://postgres:postgres@localhost:5433/postgres'

engine = create_engine(db_string)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()
