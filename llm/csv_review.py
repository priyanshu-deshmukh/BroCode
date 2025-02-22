import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Download stopwords and VADER if not already available
nltk.download("stopwords")
nltk.download("vader_lexicon")
stop_words = set(stopwords.words("english"))


def clean_text(text):
    """Cleans review text by removing punctuation, converting to lowercase, and removing stopwords."""
    text = re.sub(r"[^a-zA-Z0-9\s]", "", str(text).lower())  # Remove special characters
    text = " ".join(word for word in text.split() if word not in stop_words)  # Remove stopwords
    return text


def perform_sentiment_analysis(df):
    """Performs sentiment analysis and labels reviews as Positive, Neutral, or Negative."""
    analyzer = SentimentIntensityAnalyzer()
    df["sentiment_score"] = df["cleaned_review"].apply(lambda x: analyzer.polarity_scores(x)["compound"])

    # Categorize into Positive, Neutral, or Negative
    def label_sentiment(score):
        if score > 0.05:
            return "Positive"
        elif score < -0.05:
            return "Negative"
        else:
            return "Neutral"

    df["sentiment_label"] = df["sentiment_score"].apply(label_sentiment)
    return df


def extract_top_keywords(df, num_keywords=10):
    """Extracts the top keywords using TF-IDF."""
    vectorizer = TfidfVectorizer(max_features=20)
    tfidf_matrix = vectorizer.fit_transform(df["cleaned_review"])
    feature_names = vectorizer.get_feature_names_out()

    keywords = np.argsort(np.asarray(tfidf_matrix.sum(axis=0)).ravel())[::-1][:num_keywords]
    return [feature_names[i] for i in keywords]


def get_sentiment_trend(df):
    """Returns sentiment trend data grouped by date."""
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])  # Remove rows with invalid dates
    return df.groupby(df["date"].dt.date)["sentiment_score"].mean().reset_index()


def analyze_reviews(csv_file):
    """Main function to analyze customer reviews."""
    # Load CSV file
    df = pd.read_csv(csv_file)

    # Preprocess text data
    df["cleaned_review"] = df["review_text"].astype(str).apply(clean_text)

    # Perform sentiment analysis
    df = perform_sentiment_analysis(df)

    # Extract top keywords
    top_keywords = extract_top_keywords(df)

    # Get sentiment distribution
    sentiment_counts = df["sentiment_label"].value_counts().to_dict()

    # Get sentiment trend data
    sentiment_trend = get_sentiment_trend(df)

    return {
        "sentiment_distribution": sentiment_counts,
        "top_keywords": top_keywords,
        "sentiment_trend": sentiment_trend,
        "processed_data": df
    }

if __name__ == '__main__':

    # Run the analysis
    results = analyze_reviews("a.csv")

    # Print key insights
    print("\n🔹 **Sentiment Distribution:**", results["sentiment_distribution"])
    print("\n🔹 **Top Keywords:**", results["top_keywords"])
    print("\n🔹 **Sentiment Trend Data (first 5 rows):**")
    print(results["sentiment_trend"].head())

