import scipy
import sklearn
import seaborn
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

filepath = "#bostoncalling_1000.json"

with open(filepath) as data_file:
    tweets = []
    for line in data_file:
        tweets.append(json.loads(line.rstrip('\n')))
		
nFeatures = 20000 # the total number of features, these are the most frequent words in the dataset
tfVectorizer = CountVectorizer(max_df=0.95,  # features that appear in more than 95% of documents are discarded
                                min_df=2,     # features that appear in fewer than 2 documents are discarded
                                max_features=nFeatures,
                                stop_words='english')

vectors = tfVectorizer.fit_transform(tweets[0])
vectors.shape

nTopics = 20
nTopWords = 20

lda = LatentDirichletAllocation(n_topics=nTopics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
lda.fit(vectors)

tipsFeatures = tfVectorizer.get_feature_names()

def printTopWords(model, featureNames, nTopWords):
    """Helper function to print top words per topic."""
    for topicID, topic in enumerate(model.components_):
        print "Topic #%d:" % topicID
        print ", ".join([featureNames[i] for i in topic.argsort()[:-nTopWords-1:-1]])
    print
	
print "Topics in LDA model:"
printTopWords(lda, tipsFeatures, nTopWords)

