from sqlalchemy import Column, Integer, String
from app.database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False)
    conference = Column(String, nullable=True)
    division = Column(String, nullable=True)