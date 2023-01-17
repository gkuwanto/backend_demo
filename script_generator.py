
def generate_download_script(job):
    print(job)
    script_to_run = f""" #!/bin/bash
    mkdir -p XLM/data/{job.left_language_id}-{job.right_language_id}/mono
    qsub download_drive.sh {job.monolingual_left_uploadpath}
    qsub download_drive.sh {job.monolingual_right_uploadpath}
    qsub download_drive.sh {job.parallel_uploadpath}
    qsub download_drive.sh {job.word_dictionary_uploadpath}
    qsub download_drive.sh {job.validation_uploadpath}
    qsub download_drive.sh {job.test_uploadpath}
    qsub end_to_end.sh {job.left_language_id} {job.right_language_id}"""
    return script_to_run