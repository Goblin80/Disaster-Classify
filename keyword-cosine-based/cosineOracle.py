import numpy
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import EnglishStemmer

class CosineOracle:
    stemmer = EnglishStemmer()
    analyzer = TfidfVectorizer().build_analyzer()
    ner = spacy.load('en')
    
    def __init__(self, train_data, test_data, tag='NO TAG', NER=False):
        self.tag = tag
        self.z = CosineOracle._ner_words if NER else CosineOracle._stemmed_words
        self.vectorizer = TfidfVectorizer(stop_words='english',
                                          analyzer=self.z)
        self.train_data = train_data
        self.test_data = test_data
        self._fit()
        
    def _fit(self):
        self.train_matrix = self.vectorizer.fit_transform(self.train_data)
    
    def is_relevant(self, sample, THRESHOLD = 0.5):
        sample_matrix = self.vectorizer.transform([sample])
        t = max(cosine_similarity(self.train_matrix, sample_matrix))
        return (t >= THRESHOLD, t)
    
    def precision(self, THRESHOLD = 0.5):
        res = [self.is_relevant(x, THRESHOLD)[0] for x in self.test_data]
        return res.count(True) / len(res)

    def _stemmed_words(text):
        return (CosineOracle.stemmer.stem(word) for word in CosineOracle.analyzer(text))
    
    def _ner_words(text):
        return (str(word).lower().strip() for word in CosineOracle.ner(text).ents)

