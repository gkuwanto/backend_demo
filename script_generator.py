
def generate_download_script(job):
    script_to_run = (f"""#!/bin/bash
mkdir -p datadir/{job.left_language_id}-{job.right_language_id}/mono
mkdir -p datadir/{job.left_language_id}-{job.right_language_id}/para
qsub download_drive.sh {job.monolingual_left_uploadpath} datadir/{job.left_language_id}-{job.right_language_id}/mono
qsub download_drive.sh {job.monolingual_right_uploadpath} datadir/{job.left_language_id}-{job.right_language_id}/mono
qsub download_drive.sh {job.parallel_uploadpath} datadir/{job.left_language_id}-{job.right_language_id}/para
qsub download_drive.sh {job.word_dictionary_uploadpath} datadir/{job.left_language_id}-{job.right_language_id}/dict
qsub download_drive.sh {job.validation_uploadpath} datadir/{job.left_language_id}-{job.right_language_id}/para
qsub download_drive.sh {job.test_uploadpath} datadir/{job.left_language_id}-{job.right_language_id}/para
qsub end_to_end.sh {job.left_language_id} {job.right_language_id}"""
    )
    return script_to_run

def generate_preprocess_script(job):
    script_to_run = f"""#!/bin/bash
mkdir -p XLM/data/{job.left_language_id}-{job.right_language_id}/mono
mkdir -p XLM/data/{job.left_language_id}-{job.right_language_id}/para
qsub download_drive.sh {job.monolingual_left_uploadpath}
qsub download_drive.sh {job.monolingual_right_uploadpath}
qsub download_drive.sh {job.parallel_uploadpath}
qsub download_drive.sh {job.word_dictionary_uploadpath}
qsub download_drive.sh {job.validation_uploadpath}
qsub download_drive.sh {job.test_uploadpath}
qsub end_to_end.sh {job.left_language_id} {job.right_language_id}"""
    return script_to_run