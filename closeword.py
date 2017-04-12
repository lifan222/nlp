# -*- coding: utf-8 -*-
from gensim.models import word2vec
import logging
import sys
import codecs
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = word2vec.Word2Vec.load("jawiki_wakati.model")
argvs = sys.argv
results = model.most_similar(positive=argvs[1], topn=1000)

closewords = {}

for result in results:
    closewords[model.similarity(result[0], "契丹文字")] = result[0]

toppecents = sorted(closewords.keys())
toppecents.reverse()

for index, val in enumerate(toppecents):
    if index < 100:
        print(index, closewords[val], val)
