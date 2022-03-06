"""
Convert pickled embeddings (I think they were tensors? I wrote this script a while ago)
from msg_similarity_use.py to pickled lists, since I had issues loading the former
in an older version of the pickle module.
"""
import pickle
import json
import csv

MESSAGES = list(csv.reader(open("messages_all.txt.alphaonly.csv", "r")))
SCRATCH_DIR = "./scratch"
OTHER_SCRATCH_DIR = "./scratch_arrays"

for message in MESSAGES:
    with open(f"{SCRATCH_DIR}/embedding.{message[0]}.pkl", "rb") as picklefile:
        embedding = pickle.load(picklefile).numpy().tolist()
        with open(f"{OTHER_SCRATCH_DIR}/embedding.{message[0]}.pkl", "wb") as new_picklefile:
            pickle.dump(embedding, new_picklefile)
            print(message[0])