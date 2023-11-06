import ssl
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
from nltk.corpus import wordnet as wn

# nltk.download('wordnet')
# nltk.download('stopwords')


def clean_synset(synset):
    return synset.name().lower().split('.')[0].replace('_', ' ')


def predict_word(desc, pos):
    best_synset = None
    best_score  = 0

    s1 = ' '.join(set([word for word in desc.lower().split() if word not in stopwords.words('english')]))
    for synset in wn.all_synsets(pos):
        s2 = ' '.join(set([word for word in synset.definition().lower().split() if word not in stopwords.words('english')]))
        similarity = fuzz.token_set_ratio(s1, s2)

        if similarity > best_score:
            best_score = similarity
            best_synset = synset

    print(f"best score: {best_score}")
    return best_synset


def get_pos(pos):
    match pos:
        case 'noun':
            return 'n'
        case 'verb':
            return 'v'
        case 'adjective':
            return 'a'
        case 'adverb':
            return 'r'
        

def check_synonyms(synset):

    synonyms = wn.synsets(clean_synset(synset))
    for s in synonyms:
        if synset.pos() == s.pos() and clean_synset(synset) != clean_synset(synset):
            print("Let's try again.")
            correct = input(f"Is '{clean_synset(s)}' your word? (Yes/No) ").lower()
            if correct == "yes":
                return True
    
    print("Sorry I couldn't help")
    return False


def start_app():
    input_desc = input("Describe the word you are thinking of: ")
    input_pos = get_pos(input("What part of speech is the word? ").lower())
    guess = predict_word(input_desc, input_pos)

    correct_word = input(f"Is '{clean_synset(guess)}' your word? (Yes/No) ").lower()

    if correct_word == "no":
        correct = check_synonyms(guess)

    if correct == False:
        try_again = input("Would like to try again? (Yes/No) ").lower()
        if try_again == "yes":
            start_app()


if __name__ == "__main__":
    start_app()
