from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=False, index=False)
    experiment_name = Column(String(255), unique=True, index=True, default="exp_1")
    left_language_id = Column(String(255), unique=False)
    right_language_id = Column(String(255), unique=False)
    monolingual_left_uploadpath = Column(String(255), unique=False, default="UNUSED")
    monolingual_right_uploadpath = Column(String(255), unique=False, default="UNUSED")
    parallel_uploadpath = Column(String(255), unique=False, default="UNUSED")
    word_dictionary_uploadpath = Column(String(255), unique=False, default="UNUSED")
    validation_uploadpath = Column(String(255), unique=False, default="UNUSED")
    test_uploadpath = Column(String(255), unique=False, default="UNUSED")
    
    status = Column(Integer, default=0)
    # Status Code Meaning
    # 0: Not Started
    # 1: Downloading Data
    # 2: Finish Downloading Data
    # -2: Failed Downloading Data
    # 3: Preprocessing Data
    # 4: Finish Preprocessing Data
    # -4: Failed Preprocessing Data
    # 5: Training Model
    # 6: Finish Training Model
    # -6: Failed To Use model
    # 7: Ready to use model

