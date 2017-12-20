from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, scoped_session, sessionmaker

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('data.id'))
    created_on = Column(DateTime, default=func.now())
    data = Column(Text)
    list_id = Column(Integer, ForeignKey('list.id'))

    list = relationship('TaskList', back_populates='data')

class TaskList(Base):
    __tablename__ = 'list'
    id = Column(Integer, primary_key=True)
    secret = Column(String)
    created_on = Column(DateTime, default=func.now())

    data = relationship('Data', back_populates='list')
