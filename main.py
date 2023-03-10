from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

from fastapi.middleware.cors import CORSMiddleware


from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
from const import SUPPORTED_LANG
from utils import verify_link

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
print("Server Running")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://gkuwanto.github.io/frontend/",
    "https://gkuwanto.github.io/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def hello_world():
    return {"Hello": "World"}

@app.post("/jobs/", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    monolingual_left_id = verify_link(job.monolingual_left_uploadpath)
    if not monolingual_left_id:
        raise HTTPException(status_code=400, detail = "Invalid monolingual_left_uploadpath")
    
    monolingual_right_id = verify_link(job.monolingual_right_uploadpath)
    if not monolingual_right_id:
        raise HTTPException(status_code=400, detail = "Invalid monolingual_right_uploadpath")
    
    parallel_id = verify_link(job.parallel_uploadpath)
    if not parallel_id:
        raise HTTPException(status_code=400, detail = "Invalid parallel_uploadpath")
    
    word_dictionary_id = verify_link(job.word_dictionary_uploadpath)
    if not word_dictionary_id:
        raise HTTPException(status_code=400, detail = "Invalid word_dictionary_uploadpath")
    
    validation_id = verify_link(job.validation_uploadpath)
    if not validation_id:
        raise HTTPException(status_code=400, detail = "Invalid validation_uploadpath")
    
    test_id = verify_link(job.test_uploadpath)
    if not test_id:
        raise HTTPException(status_code=400, detail = "Invalid test_uploadpath")
    new_job = schemas.JobCreate(
        email= job.email,
        left_language_id= job.left_language_id,
        right_language_id = job.right_language_id,
        monolingual_left_uploadpath = monolingual_left_id,
        monolingual_right_uploadpath = monolingual_right_id,
        parallel_uploadpath = parallel_id,
        word_dictionary_uploadpath = word_dictionary_id,
        validation_uploadpath = validation_id,
        test_uploadpath = test_id
    )
    return crud.create_job(db=db, job=new_job)


@app.post("/predict/", response_model=schemas.Predict)
def create_predict(job: schemas.Predict, db: Session = Depends(get_db)):
    
    test_id = verify_link(job.test_set)
    if not test_id:
        raise HTTPException(status_code=400, detail = "Invalid test_set")
    new_job = schemas.Predict(
        email= job.email,
        direction = job.direction,
        experiment_name = job.experiment_name,
        test_set = test_id
    )
    return crud.create_predict(db=db, pred=new_job)


@app.get("/jobs/", response_model=List[schemas.Job])
def read_jobs(db: Session = Depends(get_db)):
    jobs = crud.get_job_by_status(db, status=0)
    return jobs

@app.get("/to_preprocess/", response_model=List[schemas.Job])
def read_jobs(db: Session = Depends(get_db)):
    jobs = crud.get_job_by_status(db, status=2)
    return jobs

@app.get("/to_train/", response_model=List[schemas.Job])
def read_jobs(db: Session = Depends(get_db)):
    jobs = crud.get_job_by_status(db, status=4)
    return jobs

@app.get("/to_finalize/", response_model=List[schemas.Job])
def read_jobs(db: Session = Depends(get_db)):
    jobs = crud.get_job_by_status(db, status=6)
    return jobs

@app.get("/models/", response_model=List[schemas.Job])
def read_jobs(db: Session = Depends(get_db)):
    jobs = crud.get_job_by_status(db, status=7)
    return jobs

@app.get("/jobs/history", response_model=List[schemas.Job])
def read_jobs_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs


@app.get("/jobs/{job_id}", response_model=schemas.JobSpecific)
def read_job_detail(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.get("/jobs/{job_id}/download", response_class=PlainTextResponse)
def read_job_download(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job_download_script(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.get("/jobs/{job_id}/preprocess", response_class=PlainTextResponse)
def read_job_preprocess(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job_preprocess_script(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.get("/jobs/{job_id}/train_lm", response_class=PlainTextResponse)
def read_job_train(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job_train_script(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job
    
@app.get("/jobs/{job_id}/train_mt", response_class=PlainTextResponse)
def read_job_train(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job_train_mt_script(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.get("/jobs/{job_id}/train_mt_sup", response_class=PlainTextResponse)
def read_job_train(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job_train_mt_sup_script(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.post("/jobs/{job_id}/update", response_model=schemas.Job)
def update_job(job_id: int, db: Session = Depends(get_db), status: int = 0):
    db_job = crud.update_job(db, job_id=job_id, status=status)
    
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job
    
