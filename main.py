import os


CDIR = os.path.dirname(os.path.realpath(__file__))
UNARXIVE_DATA = os.path.join(*[CDIR, r'data/unarxive.txt'])
COVID19_DATA = os.path.join(*[CDIR, r'data/covid19.txt'])

print('\n[1/6] Pip install requirements...\n')
os.system('pip install -r requirements.txt')

from covid19_gpt2.convenience_functions.utils import email_results
email_results(text='requirements.txt installed', name_experiment=' GPT2 generation ',
              receiver_emails=['manucelotti@gmail.com'])

print('\n[2/6] Get Articles from ArXiv...\n')
if not os.path.isfile(UNARXIVE_DATA):
    os.system('python reformat_unarxive.py')
email_results(text='unarxive reformatted', name_experiment=' GPT2 generation ',
              receiver_emails=['manucelotti@gmail.com'])

print('\n[3/6] Get Articles from Covid19...\n')
if not os.path.isfile(COVID19_DATA):
    os.system('python reformat_covid19.py')
email_results(text='covid19 reformatted', name_experiment=' GPT2 generation ',
              receiver_emails=['manucelotti@gmail.com'])

print('\n[4/6] Finetune on ArXiv...\n')
os.system('python run_language_modeling.py '
          '--output_dir=output_unarxive '
          '--model_type=gpt2 '
          '--model_name_or_path=gpt2-xl '
          '--do_train '
          '--train_data_file=data/unarxive.txt '
          '--do_eval '
          '--eval_data_file=data/unarxive_small.txt '
          '--overwrite_output_dir '
          '--block_size=200 '
          '--per_gpu_train_batch_size=4 '
          '--save_steps 200000 '
          '--num_train_epochs=1')
email_results(text='finetuned on unarxive', name_experiment=' GPT2 generation ',
              receiver_emails=['manucelotti@gmail.com'])

print('\n[5/6] Finetune on Covid19...\n')
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
email_results(text='finetuned on covid19', name_experiment=' GPT2 generation ',
              receiver_emails=['manucelotti@gmail.com'])

print('\n[6/6] Generate new literature...\n')

os.system('python run_generation.py '
          '--model_type=gpt2 '
          '--model_name_or_path=output_covid19 '
          '--k=10 '
          '--length=200 '
          '--num_return_sequences=4 '
          '--prompt="The reason why covid19 finished"')

os.system('python run_generation.py '
          '--model_type=gpt2 '
          '--model_name_or_path=output_covid19 '
          '--k=10 '
          '--length=200 '
          '--num_return_sequences=4 '
          '--prompt="An effective vaccine against covid19"')

os.system('python run_generation.py '
          '--model_type=gpt2 '
          '--model_name_or_path=output_covid19 '
          '--k=10 '
          '--length=200 '
          '--num_return_sequences=4 '
          '--prompt="The frequency in the X-rays for optimally breaking covid19"')
