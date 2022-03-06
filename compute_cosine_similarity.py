"""
Computes cosine similarity for messages that have already been turned into embeddings by USE,
and puts similar messages into a "similarity family" in the output file.

A similarity family's members are a set of messages that are similar to each other, with an
arbitrarily selected "head" that is one of those messages.

This will split the dataset into chunks of SLICE_SIZE, then compute pairwise similarity and
generate a similarity family file for each chunk.

I figured if you have large enough chunks, you can combine them reasonably accurately while
saving time by just computing the similarities of the heads of one chunk with the heads of
the other chunks, and unioning their members if the two heads are similar. This is what
collapse_similarity_families.py does with the output of this script.

In the end, I chose a SLICE_SIZE of 94500 for the Hyak supercomputer cluster, which runs
the whole script within several hours. (I may have run this on CPUs by accident, so it
might be faster if you run it with GPUs)
"""

import pickle
import csv
import os
import numpy as np
from scipy.spatial import distance

SLICE_SIZE = 100
ALL_MESSAGES = list(csv.reader(open("messages_all.txt.alphaonly.csv", "r")))
SCRATCH_DIR = "./scratch_arrays"

def get_pair_similarity(msg_idx1, msg_idx2, all_similarities):
    i = msg_idx1
    j = msg_idx2
    m = len(messages)
    return all_similarities[m * i + j - ((i + 2) * (i + 1)) // 2]

for idx in range(0, len(ALL_MESSAGES), SLICE_SIZE):
    messages = ALL_MESSAGES[idx:idx+SLICE_SIZE]
    embeddings = []

    for message in messages:
        if os.path.isfile(f"{SCRATCH_DIR}/embedding.{message[0]}.pkl"):
            with open(f"{SCRATCH_DIR}/embedding.{message[0]}.pkl", "rb") as picklefile:
                embeddings.append(pickle.load(picklefile)[0])
                print(f"Unpickled embeddings for {message[0]}")

    print("Computing similarities...")
    embeddings = np.array(embeddings)
    all_similarities = -1 * distance.pdist(embeddings, metric="cosine") + 1 # math transforms distance to similarity

    deemed_similar = set()

    with open(f"./results/alpha_similarity_families.scipy_pdist.{idx}.txt", "w") as similarity_file:
        for msg_idx, message in enumerate(messages):
            if message[0] in deemed_similar: continue

            similar_msgs = set()
            similar_msgs.add(message[0])
            print(f"Base message {message[0]}: {message[10]}")
            for other_idx, other_message in enumerate(messages):
                if msg_idx == other_idx or other_idx < msg_idx or other_message[0] in deemed_similar: continue
                
                if get_pair_similarity(msg_idx, other_idx, all_similarities) > 0.8:
                    print(f"Similar message {other_message[0]}: {other_message[10]}")
                    similar_msgs.add(other_message[0])
                    deemed_similar.update(similar_msgs)
            if len(similar_msgs) > 1:
                similarity_file.write(f"{message[0]}\t{','.join(similar_msgs)}\n")
