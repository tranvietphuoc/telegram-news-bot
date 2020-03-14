from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, String, DateTime)
from datetime import datetime


"""Create engine and declare model"""
# create an engine
engine = create_engine('sqlite:///data.db',
                       connect_args={'check_same_thread': False},
                       echo=True)


# declare a mapping
Base = declarative_base()
# create engine
Base.metadata.create_all(engine)


# declare the table to hold the infomations
class Info(Base):
    __tablename__ = 'Info'

    id = Column(Integer, primary_key=True)
    content = Column(String(200))
    link = Column(String(100))
    date_added = Column(DateTime(), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Info: link - {self.link}, content - {self.content},\
                date added - {self.date_added}'
