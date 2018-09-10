import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import EnglishStemmer

class CosineOracle:
    stemmer = EnglishStemmer()
    analyzer = TfidfVectorizer().build_analyzer()
    
    def __init__(self, train_data, test_data, tag='NO TAG'):
        self.tag = tag
        self.vectorizer = TfidfVectorizer(stop_words='english', analyzer=CosineOracle._stemmed_words)
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

