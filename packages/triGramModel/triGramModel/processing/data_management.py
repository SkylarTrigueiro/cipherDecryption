import pandas as pd
import numpy as np
import joblib

import re
import string
import random
import triGramModel.config as config

# create substitution cipher
def create_cipher():
    # one will act as the key, other as the value
    letters1 = list(string.ascii_lowercase)
    letters2 = list(string.ascii_lowercase)

    true_map = {}

    # shuffle the second set of letters
    random.shuffle(letters2)

    # fill the dictionary
    for k, v in zip(letters1, letters2):
        true_map[k] = v

    save_path = config.TRAINED_MODEL_DIR / config.TRUE_MAP_FILE_NAME
    joblib.dump(true_map,  save_path)

def encode_message(msg, true_mapping):
	
	regex = re.compile('[^a-zA-z]')
	# lowercase
	msg = msg.lower()
	# replace non-alpha characters
	msg = regex.sub(' ', msg)

	# make the encoded message
	coded_msg = []
	for ch in msg:
		coded_ch = ch # could just be a space
		if ch in true_mapping:
			coded_ch = true_mapping[ch]
		coded_msg.append(coded_ch)

	return ''.join(coded_msg)

def decode_message(msg, word_map):
	decoded_msg = []
	for ch in msg:
		decoded_ch = ch # could just be a space
		if ch in word_map:
			decoded_ch = word_map[ch]
		decoded_msg.append(decoded_ch)

	return ''.join(decoded_msg)