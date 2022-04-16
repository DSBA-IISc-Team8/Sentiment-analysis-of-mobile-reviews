import time
from app.feature_based_sentiment import generate_feature_sentiment_from_review
from app.sentiment import get_review_bert

def get_predictions(text):


  # sentiment = generate_feature_sentiment_from_review(text)
  feature_sentiment = get_review_bert(text)

  response = {
    "sentiment": "positive",
    "feature_sentiment": feature_sentiment,
  }

  return response