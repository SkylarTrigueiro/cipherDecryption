import string

def create_cipher():	

	# one will act as the key, other as the value
	letters1 = list(string.ascii_lowercase)
	letters2 = list(string.ascii_lowercase)

	true_mapping = {}

	# shuffle second set of letters
	random.shuffle(letters2)

	# populate map
	for k, v in zip(letters1, letters2):
  		true_mapping[k] = v