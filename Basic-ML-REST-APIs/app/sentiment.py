from transformers import TextClassificationPipeline, AutoTokenizer, AutoModelForSequenceClassification

def get_review_bert(review):
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment',return_tensors="pt")
    #tokenized_string = tokenizer(review, padding='max_length',truncation=True, max_length=512)

    model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment", num_labels=5)
    pipeline = TextClassificationPipeline(model=model,tokenizer=tokenizer)
    output = pipeline(review)
    #predictions = output.logits.argmax(-1)

    rating =  output[0]['label']

    if rating == '5 stars' or rating == '4 stars':
        return "positive"
    elif rating == '1 star' or rating == '2 stars':
        return "negative"
    else:
        return "neutral"