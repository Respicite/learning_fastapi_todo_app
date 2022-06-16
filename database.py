import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_string = os.environ.get('DATABASE_URL')
print(db_string)
print("=====")
if db_string.startswith("postgres://"):
    db_string.replace("postgres://", "postgresql://")
    print(db_string)

engine = create_engine(db_string)
print("=====")

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()
