# import necessary liabraries
import os
import lzma
from tqdm import tqdm
import json


# check multiple files in directory and append in files
def xz_files_in_dir(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".xz") and os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    return files

json_file = "./config_and_documentation/config.json"

# load files for config
with open(json_file) as f:
    model_data = json.load(f)
    
    
# take information for data to be stored
folder_path = model_data["Model_params"]["file_information"]["folder_path"]
output_file_train = model_data["Model_params"]["file_information"]["output_file_train"]
output_file_val = model_data["Model_params"]["file_information"]["output_file_val"]
vocab_file = model_data["Model_params"]["file_information"]["vocab_file"]

files = xz_files_in_dir(folder_path)
total_files = len(files)

# Calculate the split indices
split_index = int(total_files * 0.9) # 90% for training
files_train = files[:split_index]
files_val = files[split_index:]

# Process the files for training and validation separately
vocab = set()

# Process the training files
with open(output_file_train, "w", encoding="utf-8") as outfile:
    for filename in tqdm(files_train, total=len(files_train)):
        file_path = os.path.join(folder_path, filename)
        with lzma.open(file_path, "rt", encoding="utf-8") as infile:
            text = infile.read()
            outfile.write(text)
            characters = set(text)
            vocab.update(characters)

# Process the validation files
with open(output_file_val, "w", encoding="utf-8") as outfile:
    for filename in tqdm(files_val, total=len(files_val)):
        file_path = os.path.join(folder_path, filename)
        with lzma.open(file_path, "rt", encoding="utf-8") as infile:
            text = infile.read()
            outfile.write(text)
            characters = set(text)
            vocab.update(characters)

# Write the vocabulary to vocab.txt
with open(vocab_file, "w", encoding="utf-8") as vfile:
    for char in vocab:
        vfile.write(char + '\n')