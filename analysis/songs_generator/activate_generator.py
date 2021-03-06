import pickle
import random
import re
import sys
import numpy as np
from keras.models import load_model
from analysis.songs_generator.utils import sample, get_rand_song

maxlen = 40

with open("/Users/yiz-mac/PycharmProjects/datascienceproject/analysis/songs_generator/chars_and_indices.pcl", "rb") as f:
    chars = pickle.load(f)
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

lasttext = get_rand_song()
lasttext = re.sub(r'[^a-zA-Z0-9 \n\r,.]', '', lasttext)
model = load_model("punkgenerator_3")
start_index = random.randint(0, len(lasttext) - maxlen - 1)
for diversity in [0.9]:
    print()
    print('----- diversity:', diversity)

    generated = ''
    sentence = lasttext[start_index: start_index + maxlen]
    print('----- Generating with seed: "' + sentence + '":\n\n')

    for i in range(1200):
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
