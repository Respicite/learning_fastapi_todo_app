import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')
# if SQL_ALCHEMY_DATABASE_URL.startswith('postgres://'):
#    SQL_ALCHEMY_DATABASE_URL.replace('postgres://', 'postgresql://', 1)
# SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5433/postgres'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()
