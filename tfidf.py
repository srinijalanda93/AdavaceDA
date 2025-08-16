from sklearn.feature_extraction.text import TfidfVectorizer

class TfidfFeaturizer:
    def __init__(self, max_features=8000, ngram_range=(1,2)):
        self.v = TfidfVectorizer(max_features=max_features, ngram_range=ngram_range)
    def fit(self, texts):
        return self.v.fit(texts)
    def transform(self, texts):
        return self.v.transform(texts)
