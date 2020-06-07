import os
from covid19_gpt2.convenience_functions.utils import email_results

print('\n[1/6] Pip install requirements...\n')
#os.system('pip install -r requirements.txt')

from covid19_gpt2.convenience_functions.VeryCustomSacred import CustomExperiment

CDIR = os.path.dirname(os.path.realpath(__file__))
UNARXIVE_DATA = os.path.join(*[CDIR, r'data/unarxive.txt'])
COVID19_DATA = os.path.join(*[CDIR, r'data/covid19.txt'])

UNAMODEL = os.path.join(CDIR, 'output_unarxive')
COVMODEL = os.path.join(CDIR, 'output_covid')
for dir in [UNAMODEL, COVMODEL]:
    if not os.path.isdir(dir):
        try:
            os.mkdir(dir)
        except:
            pass

ex = CustomExperiment('stochastic_LSNN', base_dir=CDIR, GPU=0)

@ex.automain
def main():
    sacred_config_dir = os.path.join(*[CDIR, ex.observers[0].basedir, '1'])

    #email_results(text='requirements.txt installed', name_experiment=' GPT2 generation ',
    #              folders_list=[sacred_config_dir, ],
    #              receiver_emails=['manucelotti@gmail.com'])

    #print('\n[2/6] Get Articles from UnArXiv...\n')
    #if not os.path.isfile(UNARXIVE_DATA):
    #    os.system('python reformat_unarxive.py')
    #email_results(text='unarxive reformatted', name_experiment=' GPT2 generation ',
    #              folders_list=[sacred_config_dir, ],
    #              receiver_emails=['manucelotti@gmail.com'])

    print('\n[3/6] Get Articles from Covid19...\n')
    if not os.path.isfile(COVID19_DATA):
        os.system('python reformat_covid19.py')
    #email_results(text='covid19 reformatted', name_experiment=' GPT2 generation ',
    #              folders_list=[sacred_config_dir, ],
    #              receiver_emails=['manucelotti@gmail.com'])

    """
    print('\n[4/6] Finetune on UnArXiv...\n')
    os.system('python run_language_modeling.py '
              '--output_dir={} '
              '--model_type=gpt2 '
              '--model_name_or_path=gpt2 '  # gpt2-xl
              '--do_train '
              '--train_data_file=data/unarxive_small.txt '  # unarxive
              '--do_eval '
              '--eval_data_file=data/unarxive_small.txt '
              '--overwrite_output_dir '
              '--block_size=200 '
              '--per_gpu_train_batch_size=4 '
              '--save_steps 200000 '
              '--num_train_epochs=1'.format(UNAMODEL))
    #email_results(text='finetuned on unarxive', name_experiment=' GPT2 generation ',
    #              folders_list=[sacred_config_dir, ],
    #              receiver_emails=['manucelotti@gmail.com'])
    """

    print('\n[5/6] Finetune on Covid19...\n')
    os.system('python run_language_modeling.py '
              '--output_dir={} '
              '--model_type=gpt2 '
              '--model_name_or_path={} '
              '--do_train '
              '--train_data_file=data/covid19_small.txt ' # covid19
              '--do_eval '
              '--eval_data_file=data/covid19_small.txt '
              '--overwrite_output_dir '
              '--block_size=200 '
              '--per_gpu_train_batch_size=4 '
              '--save_steps 200000 '
              '--num_train_epochs=1'.format(COVMODEL, 'gpt2-xl'))   #(COVMODEL, UNAMODEL))
    #email_results(text='finetuned on covid19', name_experiment=' GPT2 generation ',
    #              folders_list=[sacred_config_dir, ],
    #              receiver_emails=['manucelotti@gmail.com'])

    print('\n[6/6] Generate new literature...\n')

    os.system('python run_generation.py '
              '--model_type=gpt2 '
              '--model_name_or_path={} '
              '--k=10 '
              '--length=200 '
              '--num_return_sequences=4 '
              '--prompt="The reason why covid19 finished"'.format(COVMODEL))

    os.system('python run_generation.py '
              '--model_type=gpt2 '
              '--model_name_or_path={} '
              '--k=10 '
              '--length=200 '
              '--num_return_sequences=4 '
              '--prompt="An effective vaccine against covid19"'.format(COVMODEL))

    os.system('python run_generation.py '
              '--model_type=gpt2 '
              '--model_name_or_path={} '
              '--k=10 '
              '--length=200 '
              '--num_return_sequences=4 '
              '--prompt="The frequency in the X-rays for optimally breaking covid19"'.format(COVMODEL))

    #email_results(
    #    folders_list=[sacred_config_dir,],
    #    name_experiment=' GPT2 generation ',
    #    receiver_emails=['manucelotti@gmail.com'])