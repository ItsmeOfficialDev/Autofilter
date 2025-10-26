from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PostedMovie(Base):
    __tablename__ = 'posted_movies'
    
    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, unique=True, index=True)
    title = Column(String)
    language = Column(String)
    year = Column(Integer)
    posted = Column(Boolean, default=False)

engine = create_engine('sqlite:///movies.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
