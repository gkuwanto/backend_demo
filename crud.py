from sqlalchemy.orm import Session

import models, schemas


def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()


def get_job_by_uploadpath(db: Session, uploadpath: str):
    return db.query(models.Job).filter(models.Job.uploadpath == uploadpath).first()


def get_job_by_status(db: Session, status: int, skip: int = 0, limit: int = 100):
    return db.query(models.Job).filter(
            models.Job.status == status
        ).offset(
            skip
        ).limit(
            limit
        ).all()

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(
        email = job.email,
        left_language_id = job.left_language_id,
        right_language_id = job.right_language_id,
        monolingual_left_uploadpath = job.monolingual_left_uploadpath,
        monolingual_right_uploadpath = job.monolingual_right_uploadpath,
        parallel_uploadpath = job.parallel_uploadpath,
        word_dictionary_uploadpath = job.word_dictionary_uploadpath,
        validation_uploadpath = job.validation_uploadpath,
        test_uploadpath = job.test_uploadpath,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job(db: Session, job_id: int, status: int):
    db_job = get_job(db, job_id)
    if db_job is not None:
        db_job.status = status
        db.commit()
        db.refresh(db_job)
    return db_job
