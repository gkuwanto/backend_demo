
def generate_download_script(job):
    script_to_run = (f"""#!/bin/bash -l
curl -X POST http://able-groove-373701.ue.r.appspot.com/jobs/{job.id}/update?status=1 -H "Content-Type: application/x-www-form-urlencoded" -d"status=1"
mkdir -p datadir/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/mono
mkdir -p datadir/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/para
mkdir -p datadir/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/dict
bash download_drive.sh {job.monolingual_left_uploadpath} datadir/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/mono/{job.left_language_id}
bash download_drive.sh {job.monolingual_right_uploadpath} datadir/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/mono/{job.right_language_id}
bash download_drive.sh {job.parallel_uploadpath} datadir/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/para/train
bash download_drive.sh {job.word_dictionary_uploadpath} datadir/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/dict
bash download_drive.sh {job.validation_uploadpath} datadir/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/para/val
bash download_drive.sh {job.test_uploadpath} datadir/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/para/test
bash end_to_end.sh {job.left_language_id} {job.right_language_id} {job.id}
"""
    )
    return script_to_run

def generate_preprocess_script(job):
    script_to_run = f"""#!/bin/bash -l
#$ -l mem_per_core=8G
#$ -pe omp 8
curl -X POST http://able-groove-373701.ue.r.appspot.com/jobs/{job.id}/update?status=3 -H "Content-Type: application/x-www-form-urlencoded" -d"status=3"
bash mine_sentence.sh {job.left_language_id} {job.right_language_id} {job.experiment_name}
bash compile.sh {job.left_language_id} {job.right_language_id} {job.experiment_name} {job.id}
cd XLM-lowreso
bash get-data-para-new.sh --src {job.left_language_id} --tgt {job.right_language_id} --exp_name {job.experiment_name} --job_id {job.id}
"""
    return script_to_run

def generate_train_script(job):
    script_to_run = f"""#!/bin/bash -l
#$ -P ivc-ml
#$ -l gpus=1
#$ -l gpu_c=7.0
#$ -q ivcbuyin
#$ -m ea
#$ -N {job.left_language_id}-{job.right_language_id}-{job.id}-lm
#$ -l h_rt=48:00:00

module load gcc/5.5.0
module load python3/3.7.7
module load cuda/10.1
module load pytorch/1.5
module load apex/0.1
module load python3/3.8.6
module load cuda/11.1
module load pytorch/1.8.1
export LANG="en_US.UTF-8"

curl -X POST http://able-groove-373701.ue.r.appspot.com/jobs/{job.id}/update?status=5 -H "Content-Type: application/x-www-form-urlencoded" -d"status=5"

python train.py \
--exp_name {job.experiment_name}lm \
--dump_path ./models/ \
--data_path './data/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/processed/{job.left_language_id}-{job.right_language_id}' \
--lgs '{job.left_language_id}-{job.right_language_id}-cos' \
--mlm_steps '{job.left_language_id},{job.right_language_id},cos' \
--emb_dim 1024 \
--n_layers 6 \
--n_heads 8 \
--dropout '0.1' \
--attention_dropout '0.1' \
--gelu_activation true \
--batch_size 32 \
--bptt 256 \
--optimizer 'adam,lr=0.0001' \
--epoch_size 200000 \
--stopping_criterion '_valid_mlm_ppl,10' \
--validation_metrics '_valid_mlm_ppl'


curl -X POST http://able-groove-373701.ue.r.appspot.com/jobs/{job.id}/update?status=6 -H "Content-Type: application/x-www-form-urlencoded" -d"status=6"
"""

    return script_to_run

def generate_train_mt_script(job):
    script_to_run = f"""#!/bin/bash -l
#$ -P ivc-ml
#$ -l gpus=1
#$ -l gpu_c=7.0
#$ -q ivcbuyin
#$ -m ea
#$ -N {job.left_language_id}-{job.right_language_id}-{job.id}-ae
#$ -l h_rt=48:00:00

module load gcc/5.5.0
module load python3/3.7.7
module load cuda/10.1
module load pytorch/1.5
module load apex/0.1
module load python3/3.8.6
module load cuda/11.1
module load pytorch/1.8.1
export LANG="en_US.UTF-8"

curl -X POST http://able-groove-373701.ue.r.appspot.com/jobs/{job.id}/update?status=5 -H "Content-Type: application/x-www-form-urlencoded" -d"status=5"
RELOAD_MODEL="$(find "/projectnb/llamagrp/gkuwanto/consumer/wiki_pipeline/XLM-lowreso/models/{job.experiment_name}lm" -name best-valid_mlm_ppl.pth | head -n1)"
python train.py \
--exp_name {job.experiment_name}mt \
--dump_path ./models/ \
--reload_model "$RELOAD_MODEL,$RELOAD_MODEL" \
--data_path './data/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/processed/{job.left_language_id}-{job.right_language_id}' \
--lgs '{job.left_language_id}-{job.right_language_id}-cos' \
--ae_steps '{job.left_language_id},{job.right_language_id}' \
--bt_steps '{job.left_language_id}-{job.right_language_id}-{job.left_language_id},{job.right_language_id}-{job.left_language_id}-{job.right_language_id}' \
--lambda_ae '0:1,100000:0.1,300000:0' \
--encoder_only false \
--emb_dim 1024 \
--n_layers 6 \
--n_heads 8 \
--dropout '0.1' \
--attention_dropout '0.1' \
--gelu_activation true \
--tokens_per_batch 4000 \
--batch_size 32 \
--bptt 256 \
--optimizer 'adam_inverse_sqrt,beta1=0.9,beta2=0.98,lr=0.0001' \
--epoch_size 200000 \
--eval_bleu true \
--max_vocab 200000 \
--stopping_criterion 'valid_{job.left_language_id}-{job.right_language_id}_mt_bleu,10' \
--validation_metrics 'valid_{job.left_language_id}-{job.right_language_id}_mt_bleu'

curl -X POST http://able-groove-373701.ue.r.appspot.com/jobs/{job.id}/update?status=6 -H "Content-Type: application/x-www-form-urlencoded" -d"status=6"
"""

    return script_to_run

def generate_train_mt_sup_script(job):
    script_to_run = f"""#!/bin/bash -l
#$ -P ivc-ml
#$ -l gpus=1
#$ -l gpu_c=7.0
#$ -q ivcbuyin
#$ -m ea
#$ -N {job.left_language_id}-{job.right_language_id}-{job.id}-mt
#$ -l h_rt=48:00:00

module load gcc/5.5.0
module load python3/3.7.7
module load cuda/10.1
module load pytorch/1.5
module load apex/0.1
module load python3/3.8.6
module load cuda/11.1
module load pytorch/1.8.1
export LANG="en_US.UTF-8"

curl -X POST http://able-groove-373701.ue.r.appspot.com/jobs/{job.id}/update?status=5 -H "Content-Type: application/x-www-form-urlencoded" -d"status=5"
RELOAD_MODEL="$(find "/projectnb/llamagrp/gkuwanto/consumer/wiki_pipeline/XLM-lowreso/models/{job.experiment_name}lm" -name best-valid_mlm_ppl.pth | head -n1)"
python train.py \
--exp_name {job.experiment_name}mt \
--dump_path ./models/ \
--reload_model "$RELOAD_MODEL,$RELOAD_MODEL" \
--data_path './data/{job.experiment_name}/{job.left_language_id}-{job.right_language_id}/processed/{job.left_language_id}-{job.right_language_id}' \
--lgs '{job.left_language_id}-{job.right_language_id}-cos' \
--mt_steps '{job.left_language_id}-{job.right_language_id},{job.right_language_id}-{job.left_language_id}' \
--bt_steps '{job.left_language_id}-{job.right_language_id}-{job.left_language_id},{job.right_language_id}-{job.left_language_id}-{job.right_language_id}' \
--lambda_ae '0:1,100000:0.1,300000:0' \
--encoder_only false \
--emb_dim 1024 \
--n_layers 6 \
--n_heads 8 \
--dropout '0.1' \
--attention_dropout '0.1' \
--gelu_activation true \
--tokens_per_batch 4000 \
--batch_size 32 \
--bptt 256 \
--optimizer 'adam_inverse_sqrt,beta1=0.9,beta2=0.98,lr=0.0001' \
--epoch_size 200000 \
--eval_bleu true \
--max_vocab 200000 \
--stopping_criterion 'valid_{job.left_language_id}-{job.right_language_id}_mt_bleu,10' \
--validation_metrics 'valid_{job.left_language_id}-{job.right_language_id}_mt_bleu'

curl -X POST http://able-groove-373701.ue.r.appspot.com/jobs/{job.id}/update?status=6 -H "Content-Type: application/x-www-form-urlencoded" -d"status=6"
"""

    return script_to_run
