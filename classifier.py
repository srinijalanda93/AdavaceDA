from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def make_linear_svm():
    return LinearSVC()

def make_logreg():
    return LogisticRegression(max_iter=1000)

def evaluate(y_true, y_pred):
    return classification_report(y_true, y_pred, digits=3)
