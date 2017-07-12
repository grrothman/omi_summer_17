import scipy
import sklearn
import seaborn
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

FILEPATH = "chance_tweet_100.txt"

nFEATURES = 20000 # the total number of features, these are the most frequent words in the dataset
MAX_DF = 0.95 # features that appear in more than X% of documents are discarded
MIN_DF = 2 # features that appear in fewer than X documents are discarded

nTOPICS = 10
nTOPWORDS = 20

def lda_model(data):

    tfVectorizer = CountVectorizer(max_df = MAX_DF,
                                    min_df = MIN_DF,
                                    max_features = nFEATURES,
                                    stop_words = 'english')

    vectors = tfVectorizer.fit_transform(data[0])
    vectors.shape


    lda = LatentDirichletAllocation(n_topics=nTOPICS, 
                                    max_iter=5,
                                    learning_method='online',
                                    learning_offset=50,
                                    random_state=0)
    lda.fit(vectors)

    tipsFeatures = tfVectorizer.get_feature_names()

    return(tipsFeatures, lda)

def printTopWords(model, featureNames, nTopWords):
    """Helper function to print top words per topic."""
    print("Topics in LDA model:")
    for topicID, topic in enumerate(model.components_):
        print("Topic #%d:" % topicID)
        print(", ".join([featureNames[i] for i in topic.argsort()[:-nTopWords-1:-1]]))
    print

def load_data(filepath) :
    with open(filepath) as data_file:
        tweet_data = []
        for line in data_file:
            tweet_data.append(json.loads(line.rstrip('\n')))

    return tweet_data

if __name__ == '__main__':
    data = load_data(FILEPATH)
    (features, model) = lda_model(data)
    printTopWords(model, features, nTOPWORDS)



