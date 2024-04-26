"""
pip install -q -U bitsandbytes
pip install -q -U git+https://github.com/huggingface/transformers.git
pip install -q -U git+https://github.com/huggingface/peft.git
pip install -q -U git+https://github.com/huggingface/accelerate.git
pip install -q -U datasets scipy ipywidgets matplotlib
"""

import pandas as pd
import os
import random
import wandb, os

# Load the CSV file into a DataFrame
dataset_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./data-cleaning/processed_dataset.csv")
df = pd.read_csv(dataset_csv_path)
chat_list = []
# Open the JSONL file for writing
with open(dataset_csv_path, 'r') as file:
    for index, row in df.iterrows():
        print('print')
        user_question = f"Peux-tu m'écrire un poème en {row['Meter']} sur {row['Theme']} comme {row['Author']} dans {row['Title']} de le recueil {row['Book']} écrit en {row['Year']} ?"
        bot_answer = f"Bien sûr:\n{row['Poem']}"
        chat_line = f"### Question: {user_question}\n ### Answer: {bot_answer}"
        print(chat_line)
        if type(chat_line) != None:
            chat_list.append(chat_line)

random.shuffle(chat_list)

# Calculate the index for splitting into train and test sets
split_index = int(len(chat_list) * 0.8)

# Split the chat list into train and test sets
train_list = chat_list[:split_index]
test_list = chat_list[split_index:]

# Convert the lists to DataFrames
train_dataset = pd.DataFrame(train_list, columns=['text'])
eval_dataset = pd.DataFrame(test_list, columns=['text'])

print(test_df)

#____

from accelerate import FullyShardedDataParallelPlugin, Accelerator
from torch.distributed.fsdp.fully_sharded_data_parallel import FullOptimStateDictConfig, FullStateDictConfig

fsdp_plugin = FullyShardedDataParallelPlugin(
    state_dict_config=FullStateDictConfig(offload_to_cpu=True, rank0_only=False),
    optim_state_dict_config=FullOptimStateDictConfig(offload_to_cpu=True, rank0_only=False),
)

accelerator = Accelerator(fsdp_plugin=fsdp_plugin)

from accelerate import FullyShardedDataParallelPlugin, Accelerator
from torch.distributed.fsdp.fully_sharded_data_parallel import FullOptimStateDictConfig, FullStateDictConfig

fsdp_plugin = FullyShardedDataParallelPlugin(
    state_dict_config=FullStateDictConfig(offload_to_cpu=True, rank0_only=False),
    optim_state_dict_config=FullOptimStateDictConfig(offload_to_cpu=True, rank0_only=False),
)

accelerator = Accelerator(fsdp_plugin=fsdp_plugin)


wandb.login()

wandb_project = "journal-finetune"
if len(wandb_project) > 0:
    os.environ["WANDB_PROJECT"] = wandb_project