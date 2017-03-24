import nltk
import random
from nltk.sentiment.vader import SentimentIntensityAnalyzer
lancaster_stemmer = nltk.stem.lancaster.LancasterStemmer()

corpus_file = open('corpus.dat', 'a+')

def sentimentAnalysis(sentence):
    #Analyzes a sentance using VADER for sentiment. Returns a dictionary that looks like this:
    #{'neg': 0.0, 'neu': 0.673, 'pos': 0.327, 'compound': 0.5267}

    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(sentence)

def getResponse(user_input):
    response = findMatch(user_input)
    corpus_file.write(user_input + '\n')
    return response

def getPOS(sentance):
    words = nltk.word_tokenize(sentance)
    words_pos = nltk.pos_tag(words)
    nouns = [word for word,pos in words_pos if (pos == 'NN') or (pos == 'NNP') or  (pos == 'NNS')]
    pronouns = [word for word,pos in words_pos if (pos == 'PRP') or (pos == 'POS') or ( pos == 'POS$')]
    verbs = [word for word,pos in words_pos if (pos == 'VBP') or (pos == 'VB') or (pos == 'VBG')]
    punctuation = [word for word,pos in words_pos if (pos == '.')]
    adjectives = [word for word,pos in words_pos if (pos == 'JJ') or (pos == 'JJR') or  (pos == 'JJS')]

    pos_output = {'nouns': nouns, 'pronouns': pronouns, 'verbs': verbs, 'adjectives': adjectives, 'punctuation': punctuation}

    #use nltk.lancaster_stemmer to lemmatize the words so it makes for consistant comparison
    for key, item in pos_output.items():
        for index, word in enumerate(item):
            pos_output[key][index] = lancaster_stemmer.stem(word)
    return pos_output

def comparisonScore(sentance1,sentance2,pos1,pos2):
    score = 0
    for element in pos1['nouns']:
        if element in pos2['nouns']:
            score = score+1
    for element in pos1['verbs']:
        if element in pos2['verbs']:
            score = score+1
    for element in pos1['adjectives']:
        if element in pos2['adjectives']:
            score = score+1

    if ('i' in pos1['pronouns']) and ('you' in pos2['pronouns']):
        score = score+2
    if ('you' in pos1['pronouns']) and ('i' in pos2['pronouns']):
        score = score+2
    if ('he' in pos1['pronouns']) and ('he' in pos2['pronouns']):
        score = score+2
    if ('she' in pos1['pronouns']) and ('she' in pos2['pronouns']):
        score = score+2
    if ('?' in pos1['punctuation']) and ('.' in pos2['punctuation']):
        score = score+4
    if ('.' in pos1['punctuation']) and ('?' in pos2['punctuation']):
        score = score+2

    sentiment_difference = abs(sentimentAnalysis(sentance1)['compound'] - sentimentAnalysis(sentance2)['compound'])

    if sentiment_difference != 0:
        score = score/sentiment_difference


    print(score)
    return score

def findMatch(sentance):
    top_score = 0
    top_response = 0

    corpus_file.seek(0)
    for line in corpus_file:
        score = comparisonScore(sentance,line,getPOS(sentance), getPOS(line))
        if score > top_score:
            top_score = score
            top_response = line

    #if there is no match found in the corpus file.
    if top_response == 0:
        top_response = "I'm Gay"
    return top_response
