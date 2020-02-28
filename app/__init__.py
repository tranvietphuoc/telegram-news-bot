from app.models import engine, Info, Base
from sqlalchemy.orm import sessionmaker

# create engine
Base.metadata.create_all(engine)

# create db session
Session = sessionmaker(autocommit=False, bind=engine)
session = Session()


