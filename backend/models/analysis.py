from sqlalchemy import Column, Integer, String, DateTime, Text
from .database import Base


class Analysis(Base):
    __tablename__ = 'analyses'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(256))
    timestamp = Column(DateTime)
    score = Column(Integer)
    quality_level = Column(String(32))
    lines = Column(Integer)
    functions = Column(Integer)
    classes = Column(Integer)
    issue_count = Column(Integer)
    analysis_summary = Column(Text)
