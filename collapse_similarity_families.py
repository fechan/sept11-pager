"""
This collapses similarity families files for chunks of the message data into one big
similarity family file by computing the cosine similarity between the embeddings for
the heads of each family in one chunk and the embeddings for the heads of each family
in the other chunk.

This saves a lot of time compared to computing similarity for every pair of hundreds
of thousands of messages. This script runs on my home computer in a matter of minutes.

With a chunk size of 94500, I ended up with only three chunks for all the ALPHA mode
messages, so I just ran this on the first two chunks, then ran the output of this
script with the last chunk to combine all three.
"""

import os
import pickle
import numpy as np
from scipy.spatial import distance

FAMILY_1 = "./results/alpha_similarity_families.scipy_pdist.combined.0-9500.txt"
FAMILY_2 = "./results/alpha_similarity_families.scipy_pdist.189000.txt"
SCRATCH_DIR = "./scratch_arrays"
OUTPUT_FAMILIES_FILE = "./results/alpha_similarity_families.scipy_pdist.combined.all.txt"

def get_family_heads_in_file(family_file):
    """Get the embedding for each family's head in the family file as an array,
    a mapping from the position in the embeddings array to its corresponding message ID,
    and the members of each family in the order they appear in the array.

    ex. if the embedding for head message ID 1234 is in index 5 of family_head_embeddings,
        you can get its message ID by using family_head_idxs[5], and the members of the
        head's family by using family_members[5]"""
    family_head_embeddings = []
    family_head_idxs = []
    family_members = []
    with open(family_file, "r") as family_file:
        for family in family_file:
            head_id, members = family.split("\t")
            family_head_idxs.append(head_id)
            family_members.append(set(members.strip().split(",")))
            if os.path.isfile(f"{SCRATCH_DIR}/embedding.{head_id}.pkl"):
                with open(f"{SCRATCH_DIR}/embedding.{head_id}.pkl", "rb") as picklefile:
                    family_head_embeddings.append(pickle.load(picklefile)[0])
                    print(f"Unpickled embeddings for {head_id}")
    return np.array(family_head_embeddings), family_head_idxs, family_members

family1_embeddings, family1_head_idxs, family1_members = get_family_heads_in_file(FAMILY_1)
family2_embeddings, family2_head_idxs, family2_members = get_family_heads_in_file(FAMILY_2)

print("Computing similarities...")
similarities = -1 * distance.cdist(family1_embeddings, family2_embeddings, metric="cosine") + 1 # math transforms distance to similarity

deemed_similar = set() # set of family heads that have already been deemed similar to another family head

with open(OUTPUT_FAMILIES_FILE, "w") as similarity_file:
    for family1_head_idx in range(len(family1_embeddings)):
        if family1_head_idx in deemed_similar: continue
        family_head_id = family1_head_idxs[family1_head_idx]
        print("Processing family from family file 1 with head ID:", family_head_id)

        family_union = family1_members[family1_head_idx] # eventually stores the union of all families that are similar to family1
        for family2_head_idx in range(len(family2_embeddings)):
            if family2_head_idx in deemed_similar: continue

            if similarities[family1_head_idx][family2_head_idx] > 0.8:
                print("\tFound similar family in family file 2 with head ID:", family2_head_idxs[family2_head_idx])
                family_union.update(family2_members[family2_head_idx])
                deemed_similar.update(family1_members[family1_head_idx])
                deemed_similar.update(family2_members[family2_head_idx])
        similarity_file.write(f"{family_head_id}\t{','.join(family_union)}\n") # this will write family1 into the file even if it's not similar to any other family
    
    # write families from family file 2 that weren't similar to any family in family file 1
    for family2_head_idx in range(len(family2_embeddings)):
        if family2_head_idx in deemed_similar: continue
        family_head_id = family2_head_idxs[family2_head_idx]
        print("Adding nonsimilar family from family file 2 with head ID:", family_head_id)
        similarity_file.write(f"{family_head_id}\t{','.join(family2_members[family2_head_idx])}\n")