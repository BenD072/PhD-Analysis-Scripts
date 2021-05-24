import nltk
from pprint import pprint
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.cluster import KMeans
from collections import Counter
from MulticoreTSNE import MulticoreTSNE as TSNE
from operator import itemgetter

# # Against Tweets
#
# # Format Data

# Import data and convert to list
df = pd.read_excel(
    '/Users/bendavies/Documents/Python /Twitter Webscraping/Analysis Scripts for Thesis/Excel Files for Thesis/Unsupportive_Tweets_For_Johnson.xlsx')
text = df['tweetText'].tolist()

# Import stop words and extend to inlcude extra terms
stop_words = nltk.corpus.stopwords.words('english')
stop_words.extend(['pm', 'boris', 'prime', 'minister', 'ruling', 'court', 'prorogue', 'prorogation',
                   'ruled', 'supreme', 'johnson', 'judgement'])


# Create function to normalize data
def normalize_document(doc):
    # lower case and remove special characters\whitespaces
    doc = re.sub(r'[^a-zA-Z0-9\s]', '', doc, re.I | re.A)
    doc = doc.lower()
    doc = doc.strip()
    # tokenize document
    tokens = nltk.word_tokenize(doc)
    # filter stopwords out of document
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # re-create document from filtered tokens
    doc = ' '.join(filtered_tokens)
    return doc


normalize_corpus = np.vectorize(normalize_document)  # Vectorize function so can be applied to whole corpus
norm_corpus = normalize_corpus(text)  # Create normalized corpus

# # Create Feature Vectors

# Create BoW model
# Max_df = remove words in more than 60% of documents
# Min_df = remove words that appear in less than X% of documents or X number of documents
cv = CountVectorizer(ngram_range=(1, 2), min_df=10, max_df=0.6, stop_words=stop_words)
cv_matrix = cv.fit_transform(norm_corpus)  # BoW matrix

# Create similarity matrix based on BoW model
cosine_sim_features = cosine_similarity(cv_matrix)

# # Run Initial KMeans Models - Determine Best K
#
# Loop through different values of k and plot inertia - use to determine inital best number of k

wcss = []  # Store ineteria scores

for i in range(1, 21):
    km = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    # i above is between 1-20 numbers. init parameter is the random initialization method
    # we select kmeans++ method. max_iter parameter the maximum number of iterations there can be to
    # find the final clusters when the K-meands algorithm is running. we enter the default value of 300
    # the next parameter is n_init which is the number of times the K_means algorithm will be run with
    # different initial centroid.

    km.fit(cosine_sim_features)  # Fit model

    # kmeans inertia_ attribute is:  Sum of squared distances of samples
    # to their closest cluster center. A measure of goodness for the model
    wcss.append(km.inertia_)

# Plot the elbow graph
plt.plot(range(1, 21), wcss)
plt.title('The Elbow Method Graph')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# # Run KMeans model based on best k

NUM_CLUSTERS = 7  # Choose based on eblow plot above

# Create model
km = KMeans(n_clusters=NUM_CLUSTERS, max_iter=100, n_init=50, random_state=42).fit(cosine_sim_features)

# View count of the number of tweets in each cluster
Counter(km.labels_)

# If needed, create dataframe to view text for each cluster
df = pd.DataFrame(text, columns=['text'])  # Create dataframe with original text
df['Norm_Text'] = norm_corpus  # Add normalized text
df['Cluster_Labels'] = km.labels_  # Add labels
df[df['Cluster_Labels'] == 5].head(10)  # View text under a specific label

# # Remove Cluster with Largest Number of Tweets
#
# Based on the initial kmeans model, the number of tweets in each cluster is heavily skewed. E.g. Cluster number 1 contains 1190 tweets - more than half. Upon closer analysis, these tweets tend to overlap with themes from the other clusters. Therefore determine that this large cluster is noise - tweets that contain mixed or overlapping clusters and don't belong in any one specific cluster.
#
# Therefore remove these tweets from the analysis, and then re-run the KMeans model using one less cluster than the original model. This gives clearer tweet clusters

# Put noise points in separate variable for supplementary analysis
df2 = df[df['Cluster_Labels'] == 1]
df2

# Create new dataset removing largest cluster (noise)

new_text = df[df['Cluster_Labels'] != 4]  # Create new dataframe of every cluster other than 2 (the noise cluster)
new_text = new_text['Norm_Text'].tolist()  # Convert new (normalised) text to list

# # Recreate feature vectors from new corpus and re-run KMeans


# Create Bow Model
cv = CountVectorizer(ngram_range=(1, 2), min_df=10, max_df=0.6, stop_words=stop_words)
cv_matrix = cv.fit_transform(new_text)  # Fit count vectroizer to new text

# Recreate similarity matrix from new BoW model
cosine_sim_features = cosine_similarity(cv_matrix)

# Rerun KMeans using k = one less than previous k
NUM_CLUSTERS = 6
km = KMeans(n_clusters=NUM_CLUSTERS, max_iter=100, n_init=50, random_state=42).fit(cosine_sim_features)
print(Counter(km.labels_))

# # Analysis of Clusters
#
# # Visualise Clusters on Plot
#
# The BoW vector matrix is sparse - mostly contains 0's. This produces issues for plotting the tweet clusters in vector space. We use TSNE to redcue the dimensionality of the original sparse matrix into a dense 2-D matrix (similar to prinicipal components analysis). This allows the clusters to be plotted

# Initalize tsne model. n_components sets dimensions of the space (2= 2-D)
# n_jobs sets number of processes to be run (-1 = run all)
tsne = TSNE(n_components=2, n_jobs=-1, random_state=0)
matrix_2d = tsne.fit_transform(cv_matrix.todense())  # Convert BoW model to 2D matrix

x = matrix_2d[:, 0]  # Get x-axis of matrix (used for plotting)
y = matrix_2d[:, 1]  # Get y axis of matrix
labels = km.labels_  # Labels of the k means clusters

# Below we set each cluster with a specific cluster (helpful to identify topics of overlapping clusters)
plt.scatter(matrix_2d[labels == 0, 0], matrix_2d[labels == 0, 1], s=100, c='red', label='Cluster 1')
plt.scatter(matrix_2d[labels == 1, 0], matrix_2d[labels == 1, 1], s=100, c='blue', label='Cluster 2')
plt.scatter(matrix_2d[labels == 2, 0], matrix_2d[labels == 2, 1], s=100, c='green', label='Cluster 3')
plt.scatter(matrix_2d[labels == 3, 0], matrix_2d[labels == 3, 1], s=100, c='cyan', label='Cluster 4')
plt.scatter(matrix_2d[labels == 4, 0], matrix_2d[labels == 4, 1], s=100, c='magenta', label='Cluster 5')
plt.scatter(matrix_2d[labels == 5, 0], matrix_2d[labels == 5, 1], s=100, c='black', label='Cluster 6')
plt.show()

# From the keyphrase analysis below we can see that cluster 2 (blue) and cluster 4 (cyan) both concern issues of resigning, hence the overlap

# # KeyPhrase analysis of clusters

# Create functions
# Create new dataframe from new text and labels
new_df = pd.DataFrame(new_text, columns=['text'])
new_df['Cluster'] = labels
new_df['CleanedTweets'] = new_df['text'].apply(normalize_document)


# Create functions for extracting keyphrases
def compute_ngrams(sequence, n):
    return list(zip(*(sequence[index:] for index in range(n))))


def flatten_corpus(corpus):
    return ' '.join([document.strip()
                     for document in corpus])


def get_top_ngrams(corpus, ngram_val=1, limit=5):
    corpus = flatten_corpus(corpus)
    tokens = nltk.word_tokenize(corpus)
    ngrams = compute_ngrams(tokens, ngram_val)
    ngrams_freq_dist = nltk.FreqDist(ngrams)
    sorted_ngrams_fd = sorted(ngrams_freq_dist.items(),
                              key=itemgetter(1), reverse=True)
    sorted_ngrams = sorted_ngrams_fd[0:limit]
    sorted_ngrams = [(' '.join(text), freq)
                     for text, freq in sorted_ngrams]
    return sorted_ngrams


# # Unigrams

# Loop through each cluster and print top 10 phrases
for i in range(0, 6):
    print('Getting top phrases for cluster:', i + 1)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=1, limit=10))
    print('-' * 80)

# # Bigrams

# Loop through each cluster and print top 10 phrases
for i in range(0, 6):
    print('Getting top phrases for cluster:', i + 1)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=2, limit=10))
    print('-' * 80)

# # Trigrams

# Loop through each cluster and print top 10 phrases
for i in range(0, 6):
    print('Getting top phrases for cluster:', i + 1)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=3, limit=10))
    print('-' * 80)


# From the analysis, it looks like there are 6 clusters that have some overlap between them
#
# Cluster 1
# - Concerned with brexit having nothing to do with suspending parliament
#
# Cluster 2
# - Calls for Boris to resign, specifically on the basis that he lied to the queen and broke the law
#
# Cluster 3
# - Concerned with the British people. From further looking at whole tweets from this cluster, can see that this cluster is specifically talking about the fact that Brexit vote doesn't reflect will of british people
#
# Cluster 4
# - General calls for resignation
#
# Cluster 5
# - Tweets referring to Boris as a liar
#
# Cluster 6
# - Concerned with Boris breaking the law
#
# Clusters 5 and 6 generally focussing on aspects of the transgression (lying and breaking law)


# ## Supp Analysis for Agaisnt Tweets
#
# Analysis of Noise Points

# Create functions for extracting keyphrases
def compute_ngrams(sequence, n):
    return list(zip(*(sequence[index:] for index in range(n))))


def flatten_corpus(corpus):
    return ' '.join([document.strip()
                     for document in corpus])


def get_top_ngrams(corpus, ngram_val=1, limit=5):
    corpus = flatten_corpus(corpus)
    tokens = nltk.word_tokenize(corpus)
    ngrams = compute_ngrams(tokens, ngram_val)
    ngrams_freq_dist = nltk.FreqDist(ngrams)
    sorted_ngrams_fd = sorted(ngrams_freq_dist.items(),
                              key=itemgetter(1), reverse=True)
    sorted_ngrams = sorted_ngrams_fd[0:limit]
    sorted_ngrams = [(' '.join(text), freq)
                     for text, freq in sorted_ngrams]
    return sorted_ngrams


new_text = df2['Norm_Text'].tolist()  # Convert new (normalised) text to list
cv = CountVectorizer(ngram_range=(1, 2), min_df=10, max_df=0.6, stop_words=stop_words)
cv_matrix = cv.fit_transform(new_text)  # BoW matrix

# Create similarity matrix based on BoW model
cosine_sim_features = cosine_similarity(cv_matrix)

wcss = []  # Store ineteria scores

for i in range(1, 101):
    km = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    # i above is between 1-20 numbers. init parameter is the random initialization method
    # we select kmeans++ method. max_iter parameter the maximum number of iterations there can be to
    # find the final clusters when the K-meands algorithm is running. we enter the default value of 300
    # the next parameter is n_init which is the number of times the K_means algorithm will be run with
    # different initial centroid.

    km.fit(cosine_sim_features)  # Fit model

    # kmeans inertia_ attribute is:  Sum of squared distances of samples
    # to their closest cluster center. A measure of goodness for the model
    wcss.append(km.inertia_)

# Plot the elbow graph
plt.plot(range(1, 101), wcss)
plt.title('The Elbow Method Graph')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

NUM_CLUSTERS = 20
km = KMeans(n_clusters=NUM_CLUSTERS, max_iter=100, n_init=50, random_state=42).fit(cosine_sim_features)
print(Counter(km.labels_))

new_df = pd.DataFrame(new_text, columns=['text'])
new_df['Cluster'] = km.labels_
new_df['CleanedTweets'] = new_df['text'].apply(normalize_document)

# Unigrams
for i in range(0, 20):
    print('Getting top unigrams for cluster: ', i + 1)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=1, limit=5))
    print('-' * 80)

for i in range(0, 20):
    print('Getting top bigrams for cluster: ', i + 1)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=2, limit=5))
    print('-' * 80)

for i in range(0, 20):
    print('Getting top trigrams for cluster: ', i + 1)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=3, limit=5))
    print('-' * 80)

# # Tweets in Favour
#
# # Prepare Data
#
# Note: additional words of 'keep' 'go' and 'going' were added to stopwords due to these being frequent terms across multiple clusters

# Import data and convert to list
df = pd.read_excel(
    '/Users/bendavies/Documents/Python /Twitter Webscraping/Analysis Scripts for Thesis/Excel Files for Thesis/Supportive_Tweets_For_Johnson.xlsx')
text = df['tweetText'].tolist()

# Import stop words and extend to inlcude extra terms
stop_words = nltk.corpus.stopwords.words('english')
stop_words.extend(['pm', 'boris', 'prime', 'minister', 'ruling', 'court', 'prorogue', 'prorogation',
                   'ruled', 'supreme', 'johnson', 'judgement', 'keep', 'go', 'going'])


# Create function to normalize data
def normalize_document(doc):
    # lower case and remove special characters\whitespaces
    doc = re.sub(r'[^a-zA-Z0-9\s]', '', doc, re.I | re.A)
    doc = doc.lower()
    doc = doc.strip()
    # tokenize document
    tokens = nltk.word_tokenize(doc)
    # filter stopwords out of document
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # re-create document from filtered tokens
    doc = ' '.join(filtered_tokens)
    return doc


normalize_corpus = np.vectorize(normalize_document)  # Vectorize function so can be applied to whole corpus
norm_corpus = normalize_corpus(text)  # Create normalized corpus

# # Create Feature Vectors

# Create BoW model
# Max_df = remove words in more than 60% of documents
# Min_df = remove words that appear in less than X% of documents or X number of documents
cv = CountVectorizer(ngram_range=(1, 2), min_df=10, max_df=0.6, stop_words=stop_words)
cv_matrix = cv.fit_transform(norm_corpus)  # BoW matrix

# Create similarity matrix based on BoW model
cosine_sim_features = cosine_similarity(cv_matrix)

# # Determine best k

wcss = []  # Store ineteria scores

for i in range(1, 41):
    km = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    # i above is between 1-20 numbers. init parameter is the random initialization method
    # we select kmeans++ method. max_iter parameter the maximum number of iterations there can be to
    # find the final clusters when the K-meands algorithm is running. we enter the default value of 300
    # the next parameter is n_init which is the number of times the K_means algorithm will be run with
    # different initial centroid.

    km.fit(cosine_sim_features)  # Fit model

    # kmeans inertia_ attribute is:  Sum of squared distances of samples
    # to their closest cluster center. A measure of goodness for the model
    wcss.append(km.inertia_)

# Plot the elbow graph
plt.plot(range(1, 41), wcss)
plt.title('The Elbow Method Graph')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# # Run initial K Means model
#
# Note - based on elbow plot for tweets in favour, unclear how many clusters should be extracted. Extract 7 clusters to be consistent with against tweets

NUM_CLUSTERS = 5  # Choose based on eblow plot above

# Create model
km = KMeans(n_clusters=NUM_CLUSTERS, max_iter=100, n_init=50, random_state=42).fit(cosine_sim_features)

# View count of the number of tweets in each cluster
Counter(km.labels_)

# If needed, create dataframe to view text for each cluster
df = pd.DataFrame(text, columns=['text'])  # Create dataframe with original text
df['Norm_Text'] = norm_corpus  # Add normalized text
df['Cluster_Labels'] = km.labels_  # Add labels
df[df['Cluster_Labels'] == 1].head(10)  # View text under a specific label

# # Remove largest cluster (noise)
#
# Note: May need to change which cluster number is removed based on previous analysis

# Put noise points in separate variable for supplementary analysis
df2 = df[df['Cluster_Labels'] == 3]
df2

# Create new dataset removing largest cluster (noise)

new_text = df[df['Cluster_Labels'] != 3]  # Create new dataframe of every cluster other than 2 (the noise cluster)
new_text = new_text['Norm_Text'].tolist()  # Convert new (normalised) text to list

# # Recreate Features and KMeans Model

# Create Bow Model
cv = CountVectorizer(ngram_range=(1, 2), min_df=10, max_df=0.6, stop_words=stop_words)
cv_matrix = cv.fit_transform(new_text)  # Fit count vectroizer to new text

# Recreate similarity matrix from new BoW model
cosine_sim_features = cosine_similarity(cv_matrix)

# Rerun KMeans using k = one less than previous k
NUM_CLUSTERS = 4
km = KMeans(n_clusters=NUM_CLUSTERS, max_iter=100, n_init=50, random_state=42).fit(cosine_sim_features)
print(Counter(km.labels_))

# # Analyse Clusters

# Initalize tsne model. n_components sets dimensions of the space (2= 2-D)
# n_jobs sets number of processes to be run (-1 = run all)
tsne = TSNE(n_components=2, n_jobs=-1, random_state=0)
matrix_2d = tsne.fit_transform(cv_matrix.todense())  # Convert BoW model to 2D matrix

x = matrix_2d[:, 0]  # Get x-axis of matrix (used for plotting)
y = matrix_2d[:, 1]  # Get y axis of matrix
labels = km.labels_  # Labels of the k means clusters

# Below we set each cluster with a specific cluster (helpful to identify topics of overlapping clusters)
plt.scatter(matrix_2d[labels == 0, 0], matrix_2d[labels == 0, 1], s=100, c='red', label='Cluster 1')
plt.scatter(matrix_2d[labels == 1, 0], matrix_2d[labels == 1, 1], s=100, c='blue', label='Cluster 2')
plt.scatter(matrix_2d[labels == 2, 0], matrix_2d[labels == 2, 1], s=100, c='green', label='Cluster 3')
plt.scatter(matrix_2d[labels == 3, 0], matrix_2d[labels == 3, 1], s=100, c='cyan', label='Cluster 4')
plt.scatter(matrix_2d[labels == 4, 0], matrix_2d[labels == 4, 1], s=100, c='magenta', label='Cluster 5')
plt.scatter(matrix_2d[labels == 5, 0], matrix_2d[labels == 5, 1], s=100, c='black', label='Cluster 6')
plt.show()

# # KeyPhrase Analysis

# Create functions
# Create new dataframe from new text and labels
new_df = pd.DataFrame(new_text, columns=['text'])
new_df['Cluster'] = labels
new_df['CleanedTweets'] = new_df['text'].apply(normalize_document)


# Create functions for extracting keyphrases
def compute_ngrams(sequence, n):
    return list(zip(*(sequence[index:] for index in range(n))))


def flatten_corpus(corpus):
    return ' '.join([document.strip()
                     for document in corpus])


def get_top_ngrams(corpus, ngram_val=1, limit=5):
    corpus = flatten_corpus(corpus)
    tokens = nltk.word_tokenize(corpus)
    ngrams = compute_ngrams(tokens, ngram_val)
    ngrams_freq_dist = nltk.FreqDist(ngrams)
    sorted_ngrams_fd = sorted(ngrams_freq_dist.items(),
                              key=itemgetter(1), reverse=True)
    sorted_ngrams = sorted_ngrams_fd[0:limit]
    sorted_ngrams = [(' '.join(text), freq)
                     for text, freq in sorted_ngrams]
    return sorted_ngrams


# # Unigram

# Loop through each cluster and print top 10 unigram phrases
for i in range(0, 4):
    print('Getting top phrases for cluster:', i)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=1, limit=10))
    print('-' * 80)

# # Bigram

# Loop through each cluster and print top 10 bigram phrases
for i in range(0, 4):
    print('Getting top phrases for cluster:', i)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=2, limit=10))
    print('-' * 80)

# # Trigram

# Loop through each cluster and print top 10 trigram phrases
for i in range(0, 4):
    print('Getting top phrases for cluster:', i)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=3, limit=10))
    print('-' * 80)


# Although the cluster plot shows overlapping clusters and isn't as clear cut as the agaisnt tweets, the keyphrase analysis from each cluster does provide meaningful themes:
#
# Cluster 1:
# - Seems to be about getting us out of EU
#
# Cluster 2:
# - Concerns delivering what 17.4 million people voted for in EU referendum
#
# Cluster 3:
# - Concerns telling Boris not to give up
#
# Cluster 4:
# - Concerns telling Boris that the people are behind him/he has backing of the people
#
# Cluster 5:
# - Concerns getting Brexit done
#
# Cluster 6:
# - Concerns telling Boris to stay strong
#
#
# Generally these clusters can probably be grouped into 2 overarching categories: delivering Brexit and general statements of support

# ## Supplementary Analysis of Noise Points
#
# Analysis of Noise Points

# Create functions for extracting keyphrases
def compute_ngrams(sequence, n):
    return list(zip(*(sequence[index:] for index in range(n))))


def flatten_corpus(corpus):
    return ' '.join([document.strip()
                     for document in corpus])


def get_top_ngrams(corpus, ngram_val=1, limit=5):
    corpus = flatten_corpus(corpus)
    tokens = nltk.word_tokenize(corpus)
    ngrams = compute_ngrams(tokens, ngram_val)
    ngrams_freq_dist = nltk.FreqDist(ngrams)
    sorted_ngrams_fd = sorted(ngrams_freq_dist.items(),
                              key=itemgetter(1), reverse=True)
    sorted_ngrams = sorted_ngrams_fd[0:limit]
    sorted_ngrams = [(' '.join(text), freq)
                     for text, freq in sorted_ngrams]
    return sorted_ngrams


new_text = df2['Norm_Text'].tolist()  # Convert new (normalised) text to list
cv = CountVectorizer(ngram_range=(1, 2), min_df=10, max_df=0.6, stop_words=stop_words)
cv_matrix = cv.fit_transform(new_text)  # BoW matrix

# Create similarity matrix based on BoW model
cosine_sim_features = cosine_similarity(cv_matrix)

wcss = []  # Store ineteria scores

for i in range(1, 101):
    km = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    # i above is between 1-20 numbers. init parameter is the random initialization method
    # we select kmeans++ method. max_iter parameter the maximum number of iterations there can be to
    # find the final clusters when the K-meands algorithm is running. we enter the default value of 300
    # the next parameter is n_init which is the number of times the K_means algorithm will be run with
    # different initial centroid.

    km.fit(cosine_sim_features)  # Fit model

    # kmeans inertia_ attribute is:  Sum of squared distances of samples
    # to their closest cluster center. A measure of goodness for the model
    wcss.append(km.inertia_)

# Plot the elbow graph
plt.plot(range(1, 101), wcss)
plt.title('The Elbow Method Graph')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

NUM_CLUSTERS = 18
km = KMeans(n_clusters=NUM_CLUSTERS, max_iter=100, n_init=50, random_state=42).fit(cosine_sim_features)
print(Counter(km.labels_))

new_df = pd.DataFrame(new_text, columns=['text'])
new_df['Cluster'] = km.labels_
new_df['CleanedTweets'] = new_df['text'].apply(normalize_document)

# Unigrams
for i in range(0, 18):
    print('Getting top unigrams for cluster: ', i + 1)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=1, limit=5))
    print('-' * 80)

for i in range(0, 18):
    print('Getting top bigrams for cluster: ', i + 1)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=2, limit=5))
    print('-' * 80)

for i in range(0, 18):
    print('Getting top trigrams for cluster: ', i + 1)
    print('-' * 80)
    print(get_top_ngrams(corpus=new_df['CleanedTweets'][new_df['Cluster'] == i], ngram_val=3, limit=5))
    print('-' * 80)

