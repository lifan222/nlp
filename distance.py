# -*- coding: utf-8 -*-
from gensim.models import word2vec
import logging
import sys
import codecs
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = word2vec.Word2Vec.load("jawiki_wakati.model")
argvs = sys.argv
results = model.most_similar(positive=argvs[1], topn=100)
for result in results:
    print(result[0], result[1])
