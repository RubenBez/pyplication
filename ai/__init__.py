import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import ssl
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

class AI():
    def __init__(self):
        # Load dataset
        df = pd.read_csv("ai/training_data.csv")

        # Check the data
        print(df.head())

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download("stopwords")
        self.stop_words = set(stopwords.words("english"))
             
        # Apply preprocessing to all text data
        df["clean_text"] = df["text"].apply(self.preprocess_text)

        # Convert text to numerical representation (TF-IDF)
        self.vectorizer = TfidfVectorizer(max_features=5000)  # Use top 5000 words
        X = self.vectorizer.fit_transform(df["clean_text"]).toarray()
        y = df["label"]  # Target labels (0 = non-hotel, 1 = hotel)

        from sklearn.model_selection import train_test_split

        # Split into training (80%) and testing (20%) sets
        X_train, self.X_test, y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        self.model = MultinomialNB()
        self.model.fit(X_train, y_train)
        
    
    def preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and numbers
        text = re.sub(r"[^a-z\s]", "", text)
        # Remove stopwords
        words = [word for word in text.split() if word not in self.stop_words]
        return " ".join(words)

    def test_ai(self):
        # Predict on test data
        y_pred = self.model.predict(self.X_test)

        # Evaluate performance
        print("Accuracy:", accuracy_score(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))

    def is_hotel(self,web_page_text):
        text = self.preprocess_text(web_page_text)
        text_vectorized = self.vectorizer.transform([text]).toarray()
        prediction = self.model.predict(text_vectorized)[0]
        return True if prediction == 1 else False
        