import os

CDIR = os.path.dirname(os.path.realpath(__file__))
UNARXIVE_DATA = os.path.join(*[CDIR, r'data/unarxive.txt'])
COVID19_DATA = os.path.join(*[CDIR, r'data/covid19.txt'])

print('Get Articles from ArXiv...')
if not os.path.isfile(UNARXIVE_DATA):
    os.system('python reformat_unarxive.py')

print('Get Articles from Covid19...')
if not os.path.isfile(COVID19_DATA):
    os.system('python reformat_covid19.py')

print('Finetune on ArXiv...')
os.system('python run_language_modeling.py '
          '--output_dir=output_unarxive '
          '--model_type=gpt2 '
          '--model_name_or_path=gpt2-xl '
          '--do_train '
          '--train_data_file=data/unarxive.txt '
          '--do_eval '
          '--eval_data_file=data/small_covid19.txt '
          '--overwrite_output_dir '
          '--block_size=200 '
          '--per_gpu_train_batch_size=4 '
          '--save_steps 200000 '
          '--num_train_epochs=1')

# finetune on covid19 articles
os.system('python run_language_modeling.py '
          '--output_dir=output_covid19 '
          '--model_type=gpt2 '
          '--model_name_or_path=output_unarxive '
          '--do_train '
          '--train_data_file=data/covid19.txt '
          '--do_eval '
          '--eval_data_file=data/small_covid19.txt '
          '--overwrite_output_dir '
          '--block_size=200 '
          '--per_gpu_train_batch_size=4 '
          '--save_steps 200000 '
          '--num_train_epochs=1')
