from app.models import engine, Info, Base
from sqlalchemy.orm import sessionmaker
import time
from app.utils import save_data, generate_list_item
from app.bot import URL


# create engine
Base.metadata.create_all(engine)

# create db session
Session = sessionmaker(autocommit=False, bind=engine)
session = Session()

while True:
    save_data(URL, generate_list_item())
    time.sleep(30*60)

