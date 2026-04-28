from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle

X = ["good python developer", "bad communication"]
y = [1, 0]

vec = TfidfVectorizer()
X_vec = vec.fit_transform(X)

model = RandomForestClassifier()
model.fit(X_vec, y)

pickle.dump(model, open("model/model.pkl", "wb"))