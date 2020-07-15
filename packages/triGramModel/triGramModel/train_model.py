from triGramModel.config import config
from triGramModel.processing import data_management as dm
from triGramModel import model as m

import pickle
import sys

def run_training():

	model = m.cipherDecrypter()

	train_file = config.DATA_DIR / config.TRAIN_DATA
	model.fit(train_file)

	return model


if __name__ == '__main__':
	
	if( config.CREATE_CIPHER == True ):
		dm.create_cipher()

	true_map_loc_name = config.TRAINED_MODEL_DIR / config.TRUE_MAP_FILE_NAME
	with open( true_map_loc_name, 'rb') as f:
		true_map = pickle.load(f)

	test = config.DATA_DIR / config.TEST_DATA
	with open(test, 'r') as file:
		original_message = file.read()

	encoded_message = dm.encode_message(original_message, true_map)

	model = run_training()
	model.predict(encoded_message)

	best_map_loc_name = config.TRAINED_MODEL_DIR / config.BEST_MAP_FILE_NAME
	with open( best_map_loc_name, 'rb') as f:
		best_map = pickle.load(f)

	model.score(encoded_message, original_message, best_map, true_map)