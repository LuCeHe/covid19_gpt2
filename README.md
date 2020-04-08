# covid19

Finetuning GPT-2 on [Kaggle Covid19 dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) to generate text about the recent scientific literature. Ideally the goal is to make an automatic scientist. If it is first finetuned on a larger scientific dataset and then finetuned on the covid19 dataset the connections that the algorithm would make would be more interesting.

# how to use this code
1. create a `data` folder, download the dataset inside and unzip it
2. run `reformat_data.py`
3. run the following command for finetuning gpt2: 

```pythonscript
python run_language_modeling.py \
              --output_dir=output   \
              --model_type=gpt2   \
              --model_name_or_path=gpt2-medium \
              --do_train \
              --train_data_file=data/covid19.txt \
              --do_eval \
              --eval_data_file=data/small_covid19.txt   \
              --overwrite_output_dir \
              --block_size=200 \
              --per_gpu_train_batch_size=4  \
              --save_steps 5000 \
              --num_train_epochs=1
```

4. run the following command for generating samples from the finetuned model: 

```pythonscript
python run_generation.py \
              --model_type=gpt2 \
              --model_name_or_path=output \
              --k=10 \
              --length=200 \
              --num_return_sequences=3 \
              --prompt="The reason why covid19 finished"
```

# interesting samples

The outputs are still repetitive and not very informative. However I will put here the ones I found to be more interesting and the code used for generating it.

## sample 1

```pythonscript
python run_language_modeling.py --output_dir=output --model_type=gpt2 --model_name_or_path=gpt2-medium --do_train --train_data_file=data/covid19.txt --do_eval --eval_data_file=data/small_covid19.txt --overwrite_output_dir --block_size=200 --per_gpu_train_batch_size=4 --save_steps 5000 --num_train_epochs=1
python run_generation.py --model_type=gpt2 --model_name_or_path=output --k=10 --length=200 --num_return_sequences=3 --prompt="The reason why covid19 finished"
```

=== GENERATED SEQUENCE 3 ===
The reason why covid19 finished as the top 10 was not clear. It is possible that it was a result of the fact that many of the participants were not in the hospital and/or had to go home for other reasons. We cannot rule out the possibility of an effect due to the small number of people who were infected and/or the fact that the participants were in hospital for longer than 5 days.

Discussion

We conducted this study with a small sample size of a small sample of individuals, with a relatively large number of participants and with the aim of developing an evidence-based approach to the management of COVID-19. The findings of this study support the recommendations of the Chinese Government and WHO, which have emphasized the importance of rapid diagnosis and isolation of patients who are infected with COVID-19.The findings of this study show that the use of personal protective equipment (PPE) and contact precautions is the key to reducing the number of cases and deaths. In particular, the use of a mask


# other collections of scientific literature

- [The CORE Collection](https://core.ac.uk/services/#access-to-raw-data)
