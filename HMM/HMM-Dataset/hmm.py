# Name: Alexander Gabriel A. Aranes
# Section: CMSC 170 EF-4L
#	Responsible Use of AI:
#		Extent and Purpose of AI Use:
#		Responsible Use Justification:

from decimal import *
import re, os

# Class for Hidden Markov Model
class HiddenMarkovModel:
    # constructor
    # path: path to the dataset
    def __init__(self, path: str):
        self._path: str = path
        self.transition_matrix: dict = {}
        self.transition_count: dict = {}

    # Start training using the passed path
    def _train(self):
        # build transition model
        self._clean_data()
        self._normalize()

        self._show_freq()
        
    # normalize the transition matrix
    def _normalize(self):
        for (prev, curr), count in self.transition_matrix.items():
            total = self.transition_count.get(prev)
            self.transition_matrix[(prev, curr)] = Decimal(count) / Decimal(total)
    
    def _build_sensor_model(self):
        pass

    def _build_init_state_model(self):
        pass

    # clean the data in the path attr
    def _clean_data(self):
        # read files in the given path
        folder_items = os.listdir(self._path)
        folder_items.sort()
        for item in folder_items:
            item_path = os.path.join(self._path, item)
            self._read_file(item_path)
            # limit to 1 for debugging

    # read the contents of a file given a pah
    def _read_file(self, item_path: str):
        if not os.path.isfile(item_path): return
        with open(item_path, "r", encoding="utf-8") as f:
            #print(item_path) # debuggiong
            file_contents = f.read()
            file_contents = re.sub(r'\s', ' ', file_contents)  # replace multiple spaces with single space
            # get sentences
            sentences = re.split(r'\.\/\.', file_contents)  # split at ./. lol TT
            for sentence in sentences:
                if not sentence.strip(): continue   # remove emptyy sentence
                words = re.sub(r'[\[\]]', '',sentence.strip()) # remove brackets
                words = re.sub(r'\s+', ' ', words).split()  # replace whitspace with space
                self._process_sentence(words)
    
    # update the counts of transition and the matrix based on the word/tag pair per sentence
    def _process_sentence(self, words: list):
        prev = None
        for pair in words:
            if '/' not in pair: continue    # skip not matching word/tag 
            try: 
                word, tag = pair.rsplit('/', 1)
                word = re.sub(r'[^a-zA-Z0-9]', '', word)  # remove non-alphanumeric
                if '|' in tag:
                    tag = tag.split('|')[0]  # TODO: fix later when clarified
                if any(c in tag for c in ",`':$().#"): tag = 'SYM'
                if prev is not None:
                    # update the count
                    self.transition_count[prev] = self.transition_count.get(prev, 0) + 1
                    self.transition_matrix[(prev, tag)] = self.transition_matrix.get((prev, tag), 0) + 1
                prev = tag
            except ValueError:
                print(f"Invalid pair: {pair}")
                exit(1)
    
    # show transition matrix and count
    def _show_freq(self):
        print("Transition Matrix:")
        for k, v in self.transition_matrix.items():
            print(f"{k}: {v}")
        print("\nTransition Counts:")
        for k, v in self.transition_count.items():
            print(f"{k}: {v}")

# when run directly
if __name__ == "__main__":
    my_hmm = HiddenMarkovModel("./training/tagged/")
    my_hmm._train()