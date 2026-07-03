import string
# import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess(text):

    tokens = word_tokenize(text.lower())

    processed = []

    for token in tokens:

        if token in string.punctuation:
            continue

        if token in stop_words:
            continue

        processed.append(
            lemmatizer.lemmatize(token)
        )

    return " ".join(processed)

from rich import print
if __name__=='__main__':
    print(preprocess('What causes sensory overload?'))