from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Jyoti%401995@localhost/todoapplicationsdatabase'

# for mysql
# SQLALCHEMY_DATABASE_URL = 'mysql + pymysql://<username>:<password>@127.0.0.1:3306/<database_name>

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
