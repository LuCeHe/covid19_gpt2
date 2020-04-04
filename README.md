# covid19

Finetuning GPT-2 on [Kaggle Covid19 dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) to generate text about the recent scientific literature. 

# how to use this code
1. create a `data` folder, download the dataset inside and unzip it
2. run `reformat_data.py`
3. run the following command: 

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

# other collections of scientific literature

- [The CORE Collection](https://core.ac.uk/services/#access-to-raw-data)
