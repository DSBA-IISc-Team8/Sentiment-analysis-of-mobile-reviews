import spacy
import re
from string import punctuation
from textblob import TextBlob
from spacy.lang.en import English
from loguru import logger


# generate_feature_sentiment_from_review(text)
# returns map of key value, with key being feature and value the sentiment

# pip3 install spacy


def clean_sentences(sentences):
    # clean up sentences by removing extra or any punctuation characters
    all_sentences = []
    for sentence in sentences:
        clean_sentence = re.sub(f"[{re.escape(punctuation)}]", "", sentence)
        all_sentences.append(clean_sentence)
    return all_sentences


def form_sentences(doc):
    ### form the sentenence tokenizer including the additional punctuation marks
    default_punct_chars = ['!', '.', '?', '։', '؟', '۔', '܀', '܁', '܂', '߹',
                           '।', '॥', '၊', '။', '።', '፧', '፨', '᙮', '᜵', '᜶', '᠃', '᠉', '᥄',
                           '᥅', '᪨', '᪩', '᪪', '᪫', '᭚', '᭛', '᭞', '᭟', '᰻', '᰼', '᱾', '᱿',
                           '‼', '‽', '⁇', '⁈', '⁉', '⸮', '⸼', '꓿', '꘎', '꘏', '꛳', '꛷', '꡶',
                           '꡷', '꣎', '꣏', '꤯', '꧈', '꧉', '꩝', '꩞', '꩟', '꫰', '꫱', '꯫', '﹒',
                           '﹖', '﹗', '！', '．', '？', '𐩖', '𐩗', '𑁇', '𑁈', '𑂾', '𑂿', '𑃀',
                           '𑃁', '𑅁', '𑅂', '𑅃', '𑇅', '𑇆', '𑇍', '𑇞', '𑇟', '𑈸', '𑈹', '𑈻', '𑈼',
                           '𑊩', '𑑋', '𑑌', '𑗂', '𑗃', '𑗉', '𑗊', '𑗋', '𑗌', '𑗍', '𑗎', '𑗏', '𑗐',
                           '𑗑', '𑗒', '𑗓', '𑗔', '𑗕', '𑗖', '𑗗', '𑙁', '𑙂', '𑜼', '𑜽', '𑜾', '𑩂',
                           '𑩃', '𑪛', '𑪜', '𑱁', '𑱂', '𖩮', '𖩯', '𖫵', '𖬷', '𖬸', '𖭄', '𛲟', '𝪈',
                           '｡', '。', '\n', '....', '..', '.....', '...', ',', 'and', 'but']
    nlp = English()
    config_ = {"punct_chars": default_punct_chars}
    nlp.add_pipe('sentencizer', config=config_)
    doc = nlp(doc)
    sentences = [sent.text.strip() for sent in doc.sents]
    return sentences


def get_sentiment(polarity, subjectivity):
    # get the sentiments based on the polarity and subjectivity
    sentiment = 'Neutral'
    if polarity >= 0.5:
        sentiment = 'Positive'
    elif polarity <= -0.1:
        sentiment = 'Negative'
    if polarity + subjectivity <= 0.1 * 2:
        sentiment = 'Negative'
    if polarity + subjectivity >= 0.6 * 2:
        sentiment = 'Positive'
    return sentiment


def get_feature_and_term_from_sentence(sentences):
    ### Gets the feature and the qualitative or adjective term after tokenizing the sentences.
    ### Input is list of untokenized cleaed up sentences
    ### Output is list of key value pair set for each sentence
    debug = True
    features = []
    nlp = spacy.load("en_core_web_sm")
    for sentence in sentences:
        doc = nlp(sentence)

        # if debug:
        #   display_detail(doc)

        descriptive_term = ''
        target = ''
        negative = ''
        for token in doc:
            if token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
                target = token.text

            if token.dep_ == 'ROOT':
                # print("from root")
                # for child in token.children:
                #   print(child.dep_)

                for child in token.children:
                    if child.dep_ == 'neg':
                        negative += child.text + ' '

            if token.pos_ == 'ADJ':
                prepend = ''
                for child in token.children:
                    if child.pos_ != 'ADV':
                        continue
                    prepend += child.text + ' '
                descriptive_term = negative + prepend + token.text
                if (len(target) > 0) & (len(descriptive_term) > 0):
                    features.append({'feature': target, 'description': descriptive_term})
    # print(features)
    return features


def get_score_from_feature(features):
    # Retruns the scores for list of features
    sentiments = {}
    for feature in features:
        # print(feature)
        score = TextBlob(feature['description']).sentiment
        sentiments[feature['feature']] = get_sentiment(score[0], score[1]), score

    return sentiments


def generate_feature_sentiment_from_review(review):

  logger.info(review)

  score = []

  if len(review) > 0:
    sentences = form_sentences(review)
    cleaned_sentences = clean_sentences(sentences)
    feature_term_list = get_feature_and_term_from_sentence(cleaned_sentences)
    score = get_score_from_feature(feature_term_list)
  return score
