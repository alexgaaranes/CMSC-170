# Name: Alexander Gabriel A. Aranes
# Section: CMSC 170 EF-4L
#	Responsible Use of AI:
#		Extent and Purpose of AI Use:
#                   AI is used to format the tags to be used from the categories provided.
#                   It is also used for reviewing python syntax to implement certain parts
#                   of the code. The functions and methods explanation was provided by the AI.
#                   These review and explanation was done thru the AI overview by Google Gemini.
#		Responsible Use Justification:
#                   Every single part of this code was typed by the author without any help
#                   of any AI code completion, copy-pasting of generated code, or agentic
#                   programming. Everything is implemented from scratch without any AI assitance.
#                   Every part of the code can be explained by the author if any concern is to be raised

import re, os, sys  # sys is for args for debugging options
from decimal import *

# global tag set
tag_set = { # Used AI to format these from the site instead of doing it one by one manually 
    "CC", "CD", "DT", "EX", "FW", "IN",
    "JJ", "JJR", "JJS", "LS", "MD",
    "NN", "NNS", "NNP", "NNPS",
    "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS",
    "RP", "SYM", "TO", "UH",
    "VB", "VBD", "VBG", "VBN", "VBP", "VBZ",
    "WDT", "WP", "WP$", "WRB"
}
# encountered tags that are not considered in the exercise
other_tags = {"$", "``", "''", "(", ")", ",", "--", ".", ":"}

# Class for Hidden Markov Model
class HiddenMarkovModel:
    # NOTE:
    # path: path to the dataset for training
    # num_sentences: number of sentences read from the training path
    # tag_counter:  counts the occurence of a tag 
    # sensor_matrix:    handles the table for the sensor model
    # transition_matrix:   handles the table for the transition prob for every cat
    # initial_state_matrix: handles the table for the cat initial state prob
    # debug_word_count: for debugging, when true, write words in a separate file
    def __init__(self, path: str):
        self._path: str = path
        self.num_sentences = 0
        self.tag_counter: dict = {}

        # Models
        self.sensor_matrix: dict = {}
        self.transition_matrix: dict = {}
        self.initial_state_matrix: dict = {}

        # debugging options
        self.debug_word_count: bool = False

        # Initialize transition matrix, initial state matrix, and tag_counter
        for item_j in tag_set:
            self.transition_matrix[item_j] = {}
            self.initial_state_matrix[item_j] = 0
            self.tag_counter[item_j] = 0
            for item_k in tag_set:
                self.transition_matrix[item_j][item_k] = 0

    # ================ PUBLIC METHODS ========================

    # Start training using the passed path
    def train(self):
        output_file = open("./testing/test.out", "w")   # empty out the file
        output_file.close()
        output_file = open("./testing/test.out", "a")   # start file append
        output_file.write("Building HMM...\n\n")
        # process sys args for debugging
        if '-dw' in sys.argv: self.debug_word_count = True

        # build models
        self._clean_data()
        self._normalize()

        # write training output
        output_file.write(f"Initial state model/distribution length: {len(self.initial_state_matrix)}\n")
        output_file.write(f"Transition model/distribution dimension: {len(self.transition_matrix)} x {len(list(self.transition_matrix.values())[0])}\n")
        output_file.write(f"Sensor model/distribution dimension: {len(tag_set)} x {len(self.sensor_matrix)}\n\n")

        # used to check if SYM has any entries, seems like none
        # for item in tag_set:
        #    if self.transition_count.get(item,0) == 0: print(item)
        #print(len(list(self.transition_matrix.values())[0]))    # 36 x 36
        #self._show_freq()
        output_file.close()


    # POS tagging
    def pos_tag(self, path: str, out_path: str):
        output_file = open(out_path, "a")   # open the output file
        output_file.write("Testing HMM...")

        # process and read inputs
        input_file = open(path, "r")
        sentences = input_file.read().split('\n')

        # for every sentence, perform POS tagging
        for i in range(len(sentences)):
            sentence = sentences[i]
            if not sentence.strip(): continue   # empty sentence, skip
            output_file.write(f"\n\nSentence {i+1}: {sentence}\n")

            # convert the sentence into list of words without non-alphanumeric chars and lowercased
            sentence = [re.sub(r'[^a-zA-Z0-9]', '', word).lower() for word in sentence.split()]
            # do tagging to the sentence
            self._tag_seq(sentence, output_file)

        output_file.close() # save

    # ================ PRIVATE METHODS ========================

    # get probability of a seq given a sentence list
    def _tag_seq(self, words: list, out_file):
        sequences = [()]    # initial sequences
        for w in words:
            # get possible tags from the sensor model
            possible_tags = [(tag,) for tag in self.sensor_matrix[w].keys()]

            new_sequences = []
            for seq in sequences:   # for every current sequence
                for tag in possible_tags:   # for every tag, append it to the existing sequences
                    new_sequences.append(seq + tag)
            sequences = new_sequences   # update the sequences

        # get the probability for each sequence
        curr_max_prob: Decimal = Decimal(0)
        curr_max_index: int = 0 # keeps track the most probable sequence
        for i in range(len(sequences)): # for each sequence
            seq = sequences[i]
            running_prob: Decimal = Decimal(1)
            prev = None # keep track the prev tag
            for j in range(len(seq)):   # for each tag in the sequence
                tag = seq[j]
                if prev == None:   # possiblilty to start in the given tag
                    running_prob *= Decimal(self.initial_state_matrix[tag])
                else:
                    running_prob *= Decimal(self.transition_matrix[prev][tag])   # P(tag|prev)
                running_prob *= Decimal(self.sensor_matrix[words[j]][tag]) 
                prev = tag  # update prev 

            # check if the probability is candidate for max
            if running_prob > curr_max_prob:
                curr_max_prob = running_prob 
                curr_max_index = i
        
        # Write results to output
        out_file.write(f"Total full-sentence tag sequences: {len(sequences)}\n")
        out_file.write("Sequence with max probability:\n=>")
        max_seq = sequences[curr_max_index]
        for i in range(len(max_seq)):
            out_file.write(f" {words[i]}/{max_seq[i]}")
        out_file.write(f": {curr_max_prob}")

    # normalize the transition matrix
    def _normalize(self):
        # normalize initial state matrix
        for tag in self.initial_state_matrix:
            self.initial_state_matrix[tag] = Decimal(self.initial_state_matrix[tag]) / Decimal(self.num_sentences)

        # normalize sensor matrix
        for word, tags in self.sensor_matrix.items():
            for tag in tags:
                if self.tag_counter[tag] == 0: continue # skip
                self.sensor_matrix[word][tag] = Decimal(self.sensor_matrix[word][tag]) / Decimal(self.tag_counter[tag])
        
        # normalize transition matrix
        for k_1, v_1 in self.transition_matrix.items():
            count = sum(v_1.values())
            for k_2 in v_1.keys():
                if count == 0: continue # skip
                v_1[k_2] = Decimal(v_1[k_2]) / Decimal(count)

    # clean the data in the path attr
    def _clean_data(self):
        if self.debug_word_count: open('./words.txt', 'w').close()
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
            if '-pp' in sys.argv: print("Training data at:", item_path) # debuggiong
            file_contents = f.read()
            # get sentences
            sentences = re.split(r'\.\/\.', file_contents)  # split at ./.
            for sentence in sentences:
                if not sentence.strip(): continue   # skip emptyy sentence
                words = re.sub(r'[\[\]]', '',sentence.strip()) # remove brackets
                words = words.split()
                self._process_sentence(words)
                self.num_sentences += 1 # count num of sentences
    
    # update the counts of transition and the matrix based on the word/tag pair per sentence
    def _process_sentence(self, words: list):
        prev = None # keep track of the previous tag
        for pair in words:  # words is a sentence
            if '/' not in pair: continue    # skip not matching word/tag pattern
            try: 
                word, tag = pair.rsplit('/', 1) # remove the first / from behind (to allow 1/2/TAG)
                if tag in other_tags: continue  # skip other tags that are not part of the exercise tags

                # Clean word
                word = re.sub(r'[^a-zA-Z0-9]', '', word).lower()  # remove non-alphanumeric
                if len(word.strip()) == 0: continue # skip empty words

                # NOTE For debuggin only (write the words in a separate file)
                if self.debug_word_count and word not in self.sensor_matrix:
              	    with open('./words.txt', 'a') as f:
              	        f.write(word+'\n')

                #if tag == 'VBG|NN': raise ValueError
                if '|' in tag:  # WARNING: encountered a VBG|NN tag
                    tag = tag.split('|')[0]  # FIXME: fix later when clarified
                
                # Build transition model
                if prev is not None:
                    # update the transition model
                    self.transition_matrix[prev][tag] = self.transition_matrix[prev][tag] + 1
                else:   # Buil initial state model
                    self.initial_state_matrix[tag] = self.initial_state_matrix[tag] + 1

                # count the tag
                self.tag_counter[tag] += 1

                # build sensor model
                # NOTE: doesn't include the tags not founc to be matched with the word
                #       possible discrepancy of this is in the dimension of the sensor model
                #       not really representing the real dimensions
                #       Considering that the exercise is brute-force and no smoothing needed,
                #       this works by implementing default of 0 for non-matched tags
                self.sensor_matrix[word] = self.sensor_matrix.get(word, {})
                self.sensor_matrix[word][tag] = self.sensor_matrix[word].get(tag, 0) + 1

                # update prev
                prev = tag
            except ValueError:  # Mainly used for debugging 
                print(f"Invalid pair: {pair}")
                exit(1)
    

# when ran directly
if __name__ == "__main__":
    my_hmm = HiddenMarkovModel("./training/tagged/")
    print("Training Hidden Markov Model...")
    my_hmm.train()
    print("Training done!")
    print("Performing POS tagging...")
    my_hmm.pos_tag('./testing/test.in', "./testing/test.out")
    print("Tagging done!")
