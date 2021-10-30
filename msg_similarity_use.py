import csv
import pickle
import os
import os.path
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow_hub as hub

MESSAGES = list(csv.reader(open("messages_all.txt.alphaonly.csv", "r")))
SCRATCH_DIR = "./scratch"

deemed_similar = set() # message numbers of all messages already deemed similar to another message
similarity_families = {} # sets of messages similar to a base message, INCLUDING itself

# If script is cancelled prematurely, you can start where you left off
# You MUST delete the file if you change the number and/or content of the input messages
# changes, because base message similarity calculation will be skipped if it's already in
# here, and none of the additional messages will be added to the similarity family
if os.path.isfile("alpha_similarity_families.txt"):
    with open("alpha_similarity_families.txt", "r") as f:
        for family in f.readlines():
            base_msg, similar_msgs = family.split("\t")
            similar_msgs = set([x.strip() for x in similar_msgs.split(",")])
            deemed_similar.update(similar_msgs)
            similarity_families[base_msg] = set(similar_msgs)

model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
similarity_family_file = open("alpha_similarity_families.txt", "a")

def try_exact_match(base_msg_no, text):
    """Return a list of message numbers whose message contents match the given text exactly
    that have not already been deemed similar to another message"""
    matches = []
    for message in MESSAGES:
        if (message[0] == base_msg_no) or (message[0] in deemed_similar):
            continue
        if message[10] == text:
            matches.append(message[0])
    return matches

def add_to_similarity_family(base_msg_no, msg_no):
    """Add the given message number to the similarity family of the given base message number"""
    if base_msg_no not in similarity_families:
        similarity_families[base_msg_no] = set()
    similarity_families[base_msg_no].add(msg_no)

def get_embedding_with_caching(message_no, message_content):
    """Get the embedding for the given message and save it to scratch/cache,
    or if it has already been calculated, return the cached embedding"""
    if os.path.isfile(f"{SCRATCH_DIR}/embedding.{message_no}.pkl"):
        with open(f"{SCRATCH_DIR}/embedding.{message_no}.pkl", "rb") as picklefile:
            return pickle.load(picklefile)
    else:
        embedding = model(message_content)
        with open(f"{SCRATCH_DIR}/embedding.{message_no}.pkl", "wb") as picklefile:
            pickle.dump(embedding, picklefile)
        return embedding

for message in MESSAGES:
    if message[0] in deemed_similar: continue

    print(f"Base message {message[0]}: {message[10]}")
    embedding = get_embedding_with_caching(message[0], message[10])
    have_tried_exact_match = False # Whether we've already tried to find an exact matches for this base message

    for other_message in MESSAGES:
        if (message[0] == other_message[0]) or (other_message[0] in deemed_similar): continue

        # If there's already been a match, it's more likely that there are
        # matches that are exactly the same
        if (not have_tried_exact_match) and (message[10] == other_message[10]):
            for exact_msg in try_exact_match(message[0], message[10]):
                add_to_similarity_family(message[0], exact_msg)
                deemed_similar.add(exact_msg)
                print(f"Exact message {exact_msg}: {other_message[10]}")
            add_to_similarity_family(message[0], message[0])
            have_tried_exact_match = True
            continue # don't compute cosine similarity for other_message since we know it's the same

        other_embedding = get_embedding_with_caching(other_message[0], other_message[10])
        if cosine_similarity(embedding, other_embedding)[0][0] > 0.8:
            print(f"Similar message {other_message[0]}: {other_message[10]}")

            deemed_similar.add(message[0])
            deemed_similar.add(other_message[0])
            add_to_similarity_family(message[0], other_message[0])
            add_to_similarity_family(message[0], message[0])
    if message[0] in similarity_families:
        similarity_family_file.write(f"{message[0]}\t{','.join(similarity_families[message[0]])}\n")
        similarity_family_file.flush() # ensure the file is written to disk immediately
        os.fsync(similarity_family_file.fileno())

similarity_family_file.close()