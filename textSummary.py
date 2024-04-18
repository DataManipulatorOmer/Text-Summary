#_________________________________________________________________________________________________________________________
#Libraries
from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
#_________________________________________________________________________________________________________________________
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

def preprocessTextFunction(text):
    sentences = sent_tokenize(text)
    words = [word_tokenize(sentence.lower()) for sentence in sentences]
    stopWords = set(stopwords.words('english'))
    filteredWords = [[word for word in sentence if word.isalnum() and word not in stopWords] for sentence in words]
    return sentences, filteredWords

def sentenceSimilarityFunct(sentence1, sentence2):
    vector1 = [0] * len(set(sentence1 + sentence2))
    vector2 = [0] * len(set(sentence1 + sentence2))
    combWords = list(set(sentence1 + sentence2))
    for word in sentence1:
        vector1[combWords.index(word)] += 1
    for word in sentence2:
        vector2[combWords.index(word)] += 1
    return 1 - cosine_distance(vector1, vector2)

def similarityMatricBuilder(filteredWords):
    similarityMatrix = np.zeros((len(filteredWords), len(filteredWords)))
    for i in range(len(filteredWords)):
        for j in range(len(filteredWords)):
            if i != j:
                similarityMatrix[i][j] = sentenceSimilarityFunct(filteredWords[i], filteredWords[j])
    return similarityMatrix

def summaryGenerator(text, num_sentences=3):
    sentences, filteredWords = preprocessTextFunction(text)
    sentenceSimilarityFunct_matrix = similarityMatricBuilder(filteredWords)
    sentenceSimilarityFunct_graph = nx.from_numpy_array(sentenceSimilarityFunct_matrix)
    scores = nx.pagerank(sentenceSimilarityFunct_graph)
    rankedSentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)
    summary = ' '.join([sentence for score, sentence in rankedSentences[:num_sentences]])
    return summary

@app.route('/summarize', methods=['POST'])
def summarizedText():
    data = request.get_json()
    text = data['text']
    num_sentences = data.get('num_sentences', 3)
    summary = summaryGenerator(text, num_sentences)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
