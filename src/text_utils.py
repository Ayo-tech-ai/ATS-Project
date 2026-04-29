import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def setup_nltk():
    resources = {
        "stopwords": "corpora/stopwords",
        "wordnet": "corpora/wordnet",
        "omw-1.4": "corpora/omw-1.4",
    }
    for name, path in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)

setup_nltk()
STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in STOP_WORDS]
    tokens = [LEMMATIZER.lemmatize(word) for word in tokens]
    return " ".join(tokens)

def get_priority_matches(cv_text, jd_text, keyword_list):
    return [keyword for keyword in keyword_list if keyword in cv_text and keyword in jd_text]

def build_explanation(matches):
    if not matches:
        return "This candidate has limited direct keyword overlap with the job description."
    return "This candidate matches the job description through skills such as: " + ", ".join(matches[:5]) + "."
