# import re
# import nltk
# from nltk.corpus import stopwords
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Download stopwords
# nltk.download("stopwords")
# stop_words = set(stopwords.words("english"))

# def preprocess_text(text):
#     # Convert to lowercase
#     text = text.lower()
#     # Remove special characters and numbers
#     text = re.sub(r"[^a-z\s]", "", text)
#     # Remove stopwords
#     words = [word for word in text.split() if word not in stop_words]
#     return " ".join(words)

# # Apply preprocessing to all text data
# df["clean_text"] = df["text"].apply(preprocess_text)

# # Convert text to numerical representation (TF-IDF)
# vectorizer = TfidfVectorizer(max_features=5000)  # Use top 5000 words
# X = vectorizer.fit_transform(df["clean_text"]).toarray()
# y = df["label"]  # Target labels (0 = non-hotel, 1 = hotel)
    