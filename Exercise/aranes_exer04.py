#	Name:		Alexander Gabriel A. Aranes
#	Section:	EF-4L
#	Responsible Use of AI:
#		Extent and Purpose of AI Use:
#			AI was used to generate summary of python syntax and module usages
#			with re and os specifically. This tool is built-in within the search
#			engine used allowing for faster lookup of python syntax and semantics.
#		Responsible Use Justification:
#			Knowledge gained from the search of syntax and summary from AI, Gemini
#			specifically, is used to apply the code below. Every character and
#			main implementation of the program is made by the author and the author
#			only without relying on code generation from AI.

import re, os

class Bow:
	_bag: dict = {}
	_path: str = None

	def __init__(self, dest: str):
		self._path = dest

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

		# Get the sum of frequencies
		total_words = sum(list(self._bag.values()))

		# Write the bag in an output file
		with open("output.txt", "w") as f:
			f.write(f"Dictionary Size: {len(sorted_keys)}\n")
			f.write(f"Total Word Count: {total_words}\n\n")
			# write per key
			for k in sorted_keys:
				f.write(f"{k}: {self._bag[k]}\n")

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

# Main
if __name__ == '__main__':
	myPath = input("Enter path: ")
	myBag = Bow(myPath)
	myBag.create_Bag()
	print("Bag created")