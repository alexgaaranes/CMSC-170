#	Name:		Alexander Gabriel A. Aranes
#	Section:	EF-4L
#	Responsible Use of AI:
#		Extent and Purpose of AI Use:

#		Responsible Use Justification:
#

from decimal import *
import re, os

class Bow:
	def __init__(self, dest: str, label: str = None):
		self._path = dest
		self._label = label
		self._bag: dict = {}
		self._size: int  = None
		self._count: int = None
		self._label: str = label

	def __repr__(self):
		return f"{self._label if self._label != None else ''}\nTotal Words: {self._count}\nDictionary Size: {self._size}"

	# Callable method for creating the bag with the given path
	def create_Bag(self):
		# Load items in given dir
		folderItems = os.listdir(self._path)

		# get the absolute file path and read
		for item in folderItems:
			item_path = os.path.join(self._path, item)
			self._readFile(item_path)

		# Sort the keys
		sorted_keys = list(self._bag.keys())
		sorted_keys.sort()
		self._size = len(sorted_keys)	# set the dict size

		# Get the sum of frequencies
		total_words = sum(list(self._bag.values()))
		self._count = total_words	# set the total frequency

		# Write the bag in an output file
		with open("output.txt", "w") as f:
			f.write(f"Dictionary Size: {self._size}\n")
			f.write(f"Total Word Count: {self._count}\n\n")
			# write per key
			for k in sorted_keys:
				f.write(f"{k}: {self._bag[k]}\n")

	# Private functions used
	# Read the file from the given path with Latin-1 encoding
	def _readFile(self, item_path: str):
		if not os.path.isfile(item_path): return
		# proceed to reading if file
		with open(item_path, 'r', encoding='Latin-1') as f:
			f_content = f.read()
			tokens = self._cleanContent(f_content)
			
			# Insert in the bag
			for token in tokens:
				if token == '': continue	# skip empty tokens
				# Add token to the bag or update the frequency
				self._bag[token] = self._bag.get(token, 0) + 1

	# Clean the content by tokenizing and using regex for removing characters
	def _cleanContent(self, f_content: str):
		# tokenization
		f_content = re.sub(r"\s", ' ', f_content)
		tokens: list = f_content.split(" ")

		# remove non-alphanumeric characters
		for i in range(len(tokens)):
			tokens[i] = re.sub(r"[^A-Za-z0-9]", '', tokens[i]).lower()

		return tokens

	# Get the label
	def get_label(self) -> str:
		return self._label

	# Get the frequency of the word in the bag
	def get_freq(self, word) -> int:
		return self._bag.get(word, 0)

	# return the size
	def get_size(self) -> int:
		return self._size

	# Get the probability of the bag
	def get_probability(self, bag_size: int, smoothing: float = 0) -> Decimal:
		return Decimal((self._size + smoothing)/ (self._size + bag_size + 2*smoothing))

	# Get word probability
	def get_word_probability(self, word, bag_size, num_new_words: int = 0, smoothing: float = 0) -> Decimal:
		return Decimal((self._bag.get(word, 0) + smoothing) / ((self._count) + (smoothing*(self._size + bag_size)+num_new_words)))


# Class for the classifier
class NaiveBayes:
	# Constructor
	def __init__(self, bag1: Bow, bag2: Bow, smoothing: float = 0, threshold: float = 0.5):
		# Bags to be used
		self._spam = bag1
		self._ham = bag2

		# Laplace smoothing
		self._smoothing = smoothing

		# Threshold
		self._threshold = threshold

		# Post-training values
		_p_spam: Decimal = None
		_p_ham: Decimal = None

	def _tokenize(self, message: str):
		existing_words = []
		new_words = []
		# tokenization
		message = re.sub(r"\s", ' ', message)
		tokens: list = message.split(" ")

		# remove non-alphanumeric characters
		for i in range(len(tokens)):
			tokens[i] = re.sub(r"[^A-Za-z0-9]", '', tokens[i]).lower()
		
		# get if the word exists in the bag, if not add to new words
		for token in tokens:
			if token == '': continue	# skip empty tokens
			if (self._spam.get_freq(token) > 0
				or self._ham.get_freq(token) > 0): existing_words.append(token)	
			else: new_words.append(token)
		
		return existing_words, new_words

	# For use
	# Train the model given the spam and ham bags
	def train(self):	# by default, use smoothing passed in initializaton
		k = self._smoothing
		self._p_spam = self._spam.get_probability(self._ham.get_size(), k)
		self._p_ham = self._ham.get_probability(self._spam.get_size(), k)

	# classify message
	def classify(self, message: str) -> tuple:
		k = self._smoothing
		# Get the tokenized words
		existing, new = self._tokenize(message)
		num_new: int = len(new)	# count of new words

		p_message_g_spam: Decimal = Decimal(1)
		p_message_g_ham: Decimal = Decimal(1)
		# Get probability of message given spam
		for word in existing:
			p_message_g_spam *= self._spam.get_word_probability(word, self._ham.get_size(), num_new, k)	
		for word in new:
			p_message_g_spam *= self._spam.get_word_probability(word, self._ham.get_size(), num_new, k)	

		# Get probability of message given ham
		for word in existing:
			p_message_g_ham *= self._ham.get_word_probability(word, self._spam.get_size(), num_new, k)	
		for word in new:
			p_message_g_ham *= self._ham.get_word_probability(word, self._spam.get_size(), num_new, k)	

		# Get probability of message
		p_message: Decimal = p_message_g_spam*self._p_spam + p_message_g_ham*self._p_ham

		# Get the probability of Spam given message
		p_spam_g_message: Decimal = (p_message_g_spam*self._p_spam) / p_message

		# Return classification and probability
		classification = self._spam.get_label() if p_spam_g_message >= self._threshold else self._ham.get_label()
		return (classification, p_spam_g_message)
		


# Main
if __name__ == '__main__':
	# Get current directory
	curr_dir = os.path.dirname(os.path.abspath(__file__))

	# Create bags
	ham_bag: Bow = Bow(os.path.join(curr_dir, "ham"), "HAM")
	ham_bag.create_Bag()
	spam_bag: Bow = Bow(os.path.join(curr_dir, "spam"), "SPAM")
	spam_bag.create_Bag()

	# Print the bag details
	print(ham_bag)
	print()
	print(spam_bag)

	# Get smoothing
	# k: float = float(input("Enter Laplace smoothing level: "))
	k = 0.001

	# Create model and train
	naive_bayes = NaiveBayes(spam_bag, ham_bag, k)
	naive_bayes.train() # train

	print(f"\nk = {k}\n")
	# Classify every file in the classify dir
	folderItems = os.listdir(os.path.join(curr_dir, "classify"))
	folderItems.sort()
	for item in folderItems:
		item_path = os.path.join(curr_dir, "classify", item)
		if not os.path.isfile(item_path): continue
		with open(item_path, 'r', encoding='Latin-1') as f:
			f_content = f.read()
			result = naive_bayes.classify(f_content)
			print(f"{item}\t{result[0].capitalize()}\t{result[1]}")
