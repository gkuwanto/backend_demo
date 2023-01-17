from typing import List, Union

from pydantic import BaseModel

class JobBase(BaseModel):
    email: str


class JobCreate(JobBase):
    left_language_id: str
    right_language_id: str
    monolingual_left_uploadpath: str
    monolingual_right_uploadpath: str
    parallel_uploadpath: str
    word_dictionary_uploadpath: str
    validation_uploadpath: str
    test_uploadpath: str


class Job(JobBase):
    id: int
    status: int
    class Config:
        orm_mode = True
    
class JobSpecific(JobBase):
    # en-so-{random number}-{date}
    id: int
    status: int
    has_failed: bool
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