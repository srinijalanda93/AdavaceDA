from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self, contamination=0.1, random_state=42):
        self.clf = IsolationForest(contamination=contamination, random_state=42)
    def fit(self, X):
        self.clf.fit(X)
    def predict_flag(self, X):
        # -1 anomaly, +1 normal → convert to 0/1
        return (self.clf.predict(X) == -1).astype(int)
