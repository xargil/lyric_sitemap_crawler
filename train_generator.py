'''Example script to generate text from Nietzsche's writings.
At least 20 epochs are required before the generated text
starts sounding coherent.
It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.
If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

from __future__ import print_function

import os
import random
import sys
from utils import sample, ES_INDEX, ES_TYPE
import elasticsearch
import numpy as np
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.models import Sequential
from keras.optimizers import RMSprop
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import re
import pickle
from keras.utils.visualize_util import plot

maxlen = 40
step = 3
sentences = []
next_chars = []
lasttext = None


def handle_from_test(text):
    global chars, char_indices, indices_char, maxlen, sentences, next_chars
    # cut the text in semi-redundant sequences of maxlen characters
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])
    print('nb sequences:', len(sentences))


es = elasticsearch.Elasticsearch()
DATA_BASEPATH = os.environ.get('DATA_BASEPATH')

q = {
    "size": 5000,
    "query": {
        "function_score": {
            "query": {
                "match": {
                    "album.genre": "Hip Hop"
                }
            },
            "random_score": {"seed": 1376773391128418000}
        }
    }
}

page = es.search(index=ES_INDEX, doc_type=ES_TYPE, body=q, params={"scroll": "10m"})

sid = page['_scroll_id']
scroll_size = page['hits']['total']

# Start scrolling
charlist = set()
# while scroll_size > 0:
for _ in range(1):
    for x in page['hits']['hits']:
        text = x['_source']['lyrics']
        text = re.sub(r'[^a-zA-Z0-9 \n\r,.]', '', text)
        currchars = list(set(text))
        charlist = charlist.union(set(currchars))
        try:
            detected_lang = detect(text=text[:30])
        except LangDetectException as e:
            continue
        if detected_lang != 'en':
            continue
        lasttext = text
        handle_from_test(text)
    print("Scrolling...")
    page = es.scroll(scroll_id=sid, scroll='10m')
    # Update the scroll ID
    sid = page['_scroll_id']
    # Get the number of results that we returned in the last scroll
    scroll_size = len(page['hits']['hits'])
    print("scroll size: " + str(scroll_size))

chars = sorted(charlist)
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

with open("chars_and_indices.pcl", "wb") as f:
    pickle.dump(chars, f)
print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)
model.load_weights("/Users/yiz-mac/rapmodel_3")




# train the model, output generated text after each iteration
for iteration in range(1, 60):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y, batch_size=512, nb_epoch=1)
    model.save("/tmp/result")
    start_index = random.randint(0, len(lasttext) - maxlen - 1)

    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print()
        print('----- diversity:', diversity)

        generated = ''
        sentence = lasttext[start_index: start_index + maxlen]
        generated += sentence
        print('----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)

        for i in range(400):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.

            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()
