from sqlalchemy.orm import Session

import models, schemas, script_generator
import random, string
from datetime import datetime



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
    random_name = ''.join(random.choices(string.ascii_letters, k=6))
    left_id = job.left_language_id
    right_id = job.right_language_id
    left_id, right_id = sorted((left_id, right_id))
    db_job = models.Job(
        email = job.email,
        experiment_name = f"{left_id}-{right_id}-{random_name}-{datetime.now().strftime('%D')}",
        left_language_id = left_id,
        right_language_id = right_id,
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

def get_job_download_script(db: Session, job_id: int):
    return script_generator.generate_download_script(get_job(db, job_id))

def get_job_preprocess_script(db: Session, job_id: int):
    return script_generator.generate_preprocess_script(get_job(db, job_id))

def get_job_train_script(db: Session, job_id: int):
    return script_generator.generate_train_script(get_job(db, job_id))

def get_job_train_mt_script(db: Session, job_id: int):
    return script_generator.generate_train_mt_script(get_job(db, job_id))


def get_job_train_mt_sup_script(db: Session, job_id: int):
    return script_generator.generate_train_mt_sup_script(get_job(db, job_id))

def create_predict(db: Session, pred: schemas.Predict):
    db_job = models.Predict(
        email = pred.email,
        experiment_name = pred.experiment_name,
        direction = 0 if pred.direction == 'left' else 1,
        test_uploadpath = pred.test_set
    )
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return pred