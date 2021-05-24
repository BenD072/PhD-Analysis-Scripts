# Scripts for conducting analysis of twitter data posted in response to Boris Johnson's prorogation of Parliament
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer

# Import the dataset
# There is a total of 4511 tweets
# Take 10% to form classifier and code rest (450)
df = pd.read_excel(
    "/Users/user/Documents/Python /Twitter Webscraping/Analysis Scripts for Thesis/Excel Files for Thesis/Test_Data_For_Classifier.xlsx",
    headers=True)

# Split tweets into training and test set
# Use 80% as training set and 20% as test set
train_data, test_data, train_labels, test_labels = train_test_split(df['tweetText'], df['Labels'], test_size=0.2,
                                                                    random_state=1)

# Check data and labels are same length
print(len(train_data))
print(len(train_labels))

# Create the counter to vectorize the data
counter = CountVectorizer(ngram_range=(1, 2))  # Create counter object using unigrams and bigrams
counter.fit(train_data)  # Fit counter on the training set
train_counts = counter.transform(train_data)  # Transform training set into count vectors
test_counts = counter.transform(test_data)  # Transform testing set into count vectors
print(train_data[1])
print(train_counts[1])  # See what tweet looks like as a count vector

# Fit Logistic Regression Classifier
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
model.fit(train_counts, train_labels)
predictions = model.predict(test_counts)

# Naive Bayes
# Create the classifier and train it
classifier = MultinomialNB()  # Create classifier model
classifier.fit(train_counts, train_labels)  # Fit the model to the vector counts of the training data
predictions = classifier.predict(test_counts)  # Make a list of predictions from the vector counts of the test data

# NB gives higher accuracy at 85%
from sklearn.metrics import accuracy_score

print(accuracy_score(test_labels, predictions))

# Use classifier to predcit class for remaining tweets

# Import dataset
df2 = pd.read_excel(
    "/Users/user/Documents/Python /Twitter Webscraping/Analysis Scripts for Thesis/Excel Files for Thesis/Remaining Boris Replies for Classification.xlsx",
    headers=True)

# Create list of tweet text, classify and add back to dataframe
tweets_to_predict = df2['tweetText']

# Transform tweets into vector counts
new_tweet_counts = counter.transform(tweets_to_predict)

# Create a list of predicted labels for the new tweets
new_predictions = classifier.predict(new_tweet_counts)

# Add the labels back into the dataframe
df2["Labels"] = new_predictions

# Create datasets for supportive and unsupportive tweets
# Split into two dataframes - for and agaisnt
favour_tweets = []
against_tweets = []

for index, row in df2.iterrows():
    if row['Labels'] == 1:
        favour_tweets.append(row)
    else:
        against_tweets.append(row)

favour_tweets = pd.DataFrame(favour_tweets)
against_tweets = pd.DataFrame(against_tweets)

favour_tweets.drop('Unnamed: 0', axis=1, inplace=True)
against_tweets.drop('Unnamed: 0', axis=1, inplace=True)

# Save dataframes
favour_tweets.to_excel('Supportive_Tweets_For_Johnson.xlsx')
against_tweets.to_excel('Unsupportive_Tweets_For_Johnson.xlsx')






