from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:19990909@localhost/test?charset=utf8'

# SQL alchemy引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# sessionmaker 会话生成器
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
