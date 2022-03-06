"""
Find messages which appear to be duplicates in the messages data.
Uses TF-IDF to generate embeddings for each message, and compares
them with cosine similarity.

In the end, I decided TF-IDF wasn't good enough and switched to USE
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv

MESSAGES = csv.reader(open('messages_all.txt.alphaonly.csv', 'r'))

def tfidf_similarity(text1, text2):
    tfidf = TfidfVectorizer().fit_transform([text1, text2])
    return cosine_similarity(tfidf[0], tfidf[1])[0][0]

deemed_similar = set() # message numbers of all messages already deemed similar to another message
similarity_families = {}

for message in MESSAGES:
    if message[0] in deemed_similar:
        continue
    for other_message in MESSAGES:
        if (message[0] == other_message[0]) or (other_message[0] in deemed_similar):
            continue
        if tfidf_similarity(message[10], other_message[10]) > 0.8:
            deemed_similar.add(message[0])
            deemed_similar.add(other_message[0])
            if message[0] not in similarity_families:
                similarity_families[message[0]] = set()
            similarity_families[message[0]].add(other_message[0])
            similarity_families[message[0]].add(message[0])

with open("alpha_similarity_families.txt", "w") as f:
    for similar_set in similarity_families.items():
        f.write(",".join(str(x) for x in similar_set) + "\n")