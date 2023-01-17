from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=False, index=False)
    left_language_id = Column(String, unique=False)
    right_language_id = Column(String, unique=False)
    monolingual_left_uploadpath = Column(String, unique=False)
    monolingual_right_uploadpath = Column(String, unique=False)
    parallel_uploadpath = Column(String, unique=False)
    word_dictionary_uploadpath = Column(String, unique=False)
    validation_uploadpath = Column(String, unique=False)
    test_uploadpath = Column(String, unique=False)
    
    status = Column(Integer, default=0)

