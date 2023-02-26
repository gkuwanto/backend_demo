from typing import List, Union, Optional

from pydantic import BaseModel

class JobBase(BaseModel):
    email: str


class JobCreate(JobBase):
    left_language_id: str
    right_language_id: str
    monolingual_left_uploadpath: Optional[str] = None
    monolingual_right_uploadpath: Optional[str] = None
    parallel_uploadpath: Optional[str] = None
    word_dictionary_uploadpath: str
    validation_uploadpath: str
    test_uploadpath: str


class Job(JobBase):
    id: int
    status: int
    experiment_name: str
    class Config:
        orm_mode = True
    
class JobSpecific(JobBase):
    # en-so-{random number}-{date}
    id: int
    status: int
    experiment_name: str
    # Required
    left_language_id: str
    right_language_id: str
    word_dictionary_uploadpath: str
    validation_uploadpath: str
    test_uploadpath: str
    # Optional
    monolingual_left_uploadpath: str
    monolingual_right_uploadpath: str
    parallel_uploadpath: str
    class Config:
        orm_mode = True

class Predict(BaseModel):
    email: str
    experiment_name: str
    direction: int
    test_uploadpath: str