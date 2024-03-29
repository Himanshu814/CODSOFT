# -*- coding: utf-8 -*-
"""Movie Genre Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12jVluvqkXK8GQ6frSWc687Ukm6AwO69C

# **Movie Genre Detection**

**Importing Library**
"""

#Importing Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
import string

from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

"""**Loading Data**"""

# Load the training data

train_path = "/content/train_data.txt"
train_data = pd.read_csv(train_path, sep=':::', names=['Title', 'Genre', 'Description'], engine='python')
train_data.head(3)

from matplotlib import pyplot as plt
import seaborn as sns
_df_0.groupby('Title').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
plt.gca().spines[['top', 'right',]].set_visible(False)

# Load the test data

test_path = "/content/test_data.txt"
test_data = pd.read_csv(test_path, sep=':::', names=['Id', 'Title', 'Description'], engine='python')
test_data.head(3)

test_soln_path = "/content/test_data_solution.txt"
test_soln_data = pd.read_csv(test_soln_path, sep=':::', names=['Id', 'Title', 'Description'], engine='python')
test_soln_data.drop(test_soln_data.columns[[0, 2]], axis=1, inplace=True)
test_soln_data.rename(columns = {'Title':'Actual Genre'}, inplace = True)
test_soln_data.head(3)

"""**Visualization**"""

#Count each genre value
train_data.Genre.value_counts()

# Plot the distribution of genres using a bar plot
plt.figure(figsize=(14, 7))
counts = train_data['Genre'].value_counts()
sns.barplot(x=counts.index, y=counts, palette='mako')
plt.xlabel('Distribution of Genres', fontsize=14, fontweight='bold')
plt.ylabel('Count', fontsize=14, fontweight='bold')
plt.title('BAR CHART', fontsize=16, fontweight='bold')
plt.xticks(rotation=90, fontsize=14, fontweight='bold')
plt.show()

"""**Data Preprocessing**"""

train_data.info()

#Find null value
train_data.isnull().sum()

import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Initialize the stemmer and stop words
stemmer = LancasterStemmer()
stop_words = set(stopwords.words('english'))

# Define the clean_text function
def clean_text(text):
    text = text.lower()  # Lowercase all characters
    text = re.sub(r'@\S+', '', text)  # Remove Twitter handles
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'pic.\S+', '', text)
    text = re.sub(r"[^a-zA-Z+']", ' ', text)  # Keep only characters
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text + ' ')  # Keep words with length > 1 only
    text = "".join([i for i in text if i not in string.punctuation])
    words = nltk.word_tokenize(text)
    stopwords = nltk.corpus.stopwords.words('english')  # Remove stopwords
    text = " ".join([i for i in words if i not in stopwords and len(i) > 2])
    text = re.sub("\s[\s]+", " ", text).strip()  # Remove repeated/leading/trailing spaces
    return text

# Apply the clean_text function to the 'Description' column in the training and test data
train_data['Text_cleaning'] = train_data['Description'].apply(clean_text)
test_data['Text_cleaning'] = test_data['Description'].apply(clean_text)

# Dropping the redundant data

train_data = train_data.drop_duplicates()
print("shape",train_data.shape)

plt.title('Distribution of Text Lengths', fontsize=14, fontweight='bold')
plt.xlabel('Length', fontsize=12, fontweight='bold')
plt.ylabel('Frequency', fontsize=12, fontweight='bold')

sns.histplot(data=train_data, x='length_Text_cleaning', bins=20, kde=True, color='purple', alpha=0.5)
plt.xticks(rotation=45)
mean_length = train_data['length_Text_cleaning'].mean()
plt.axvline(mean_length, color='red', linestyle='dashed', linewidth=2)
plt.show()

# Set up the figure with two subplots
plt.figure(figsize=(5, 5))

#  Cleaned text length distribution

cleaned_lengths = train_data['Text_cleaning'].apply(len)
plt.hist(cleaned_lengths, bins=range(0, max(cleaned_lengths) + 100, 100), color='green', alpha=0.7)
plt.title('Cleaned Text Length')
plt.xlabel('Text Length')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

"""**Text Vectorization (TF-IDF)**"""

# Initialize the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the training data
X_train = tfidf_vectorizer.fit_transform(train_data['Text_cleaning'])

# Transform the test data
X_test = tfidf_vectorizer.transform(test_data['Text_cleaning'])

#Split data into train and test data
X = X_train
y = train_data["Genre"]

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size= 0.2, random_state=42)

"""**SVM**"""

import warnings
warnings.filterwarnings("ignore")

# Initialize and train a Support Vector Classifier
clf_svc = SVC()
clf_svc.fit(X_train, Y_train)

# Make predictions on the validation set
y_pred = clf_svc.predict(X_test)

# Evaluate the performance of the model
accuracy = accuracy_score(Y_test, y_pred)
print("Validation Accuracy:", accuracy)
print(classification_report(Y_test, y_pred))

accuracy_svc = accuracy_score(Y_test, y_pred)
accuracy_svc

"""**Naive Bayes**"""

import warnings
warnings.filterwarnings("ignore")

# Initialize and train a Support Vector Classifier
clf_NB = MultinomialNB()
clf_NB.fit(X_train, Y_train)

# Make predictions on the validation set
y_pred = clf_NB.predict(X_test)

# Evaluate the performance of the model
accuracy = accuracy_score(Y_test, y_pred)
print("Validation Accuracy:", accuracy)
print(classification_report(Y_test, y_pred))

accuracy_NB = accuracy_score(Y_test, y_pred)
accuracy_NB

"""**Logistic Regression**"""

# Initialize and train a Logistic Regression Classifier
clf_logreg = LogisticRegression(multi_class='multinomial', solver='sag')
clf_logreg.fit(X_train, Y_train)

# Make predictions on the validation set
y_pred = clf_logreg.predict(X_test)

# Evaluate the performance of the model
accuracy = accuracy_score(Y_test, y_pred)
print("Validation Accuracy:", accuracy)
print(classification_report(Y_test, y_pred))

accuracy_logreg = accuracy_score(Y_test, y_pred)
accuracy_logreg

"""**Comparison between SVM, Naive Bayes and Logistic Regression**"""

# Create a bar chart with different colors for each model
plt.bar('Logistic Regression', accuracy_logreg, color='blue', width=0.5)
plt.bar('Naive Bayes', accuracy_NB, color='orange', width=0.5)
plt.bar('SVM', accuracy_svc, color='green', width=0.5)

# Add labels and title
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Comparison of Accuracy')

# Show the plot
plt.show()