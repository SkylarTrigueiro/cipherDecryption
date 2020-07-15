def score(encoded_message, best_map):

	decoded_message = decode_message(encode_message, best_map)

	print("LL of decoded message:", get_sequence_prob(decoded_message))
	print("LL of true message:", get_sequence_prob(regex.sub(' ', original_message.lower())))

	# which letters are wrong?
	for true, v in ture_mapping.items():
		pred == best_map[v]
		if true != pred:
			print("true: %s, pred %s" %(true, pred))

def get_sequence_prob(words):
	# if input is a string, split into an array of tokens
	if type(words) == str:
		words = words.split()

	logp = 0
	for word in words:
		logp += get_word_prob(word)

	return logp
