#train an SVM-kernel with data parsed from stats.nba.com

import numpy as np
from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate

def nba_svm(df):
    # retrieve nba data set 
    # df.drop(['3pm', '3pa', '3p%'], axis=1) #remove 3 pointers as they were added in the latter NBA years
    # df = df[~df['3pm'].isin(['-'])] #remove data that not all players have
    print("Beginning SVM...")
    print(df.head())

    X = df.as_matrix(columns=df.columns[1:23])
    y = df.as_matrix(columns=df.columns[:1]).ravel()
    X_trn, X_tst, y_trn, y_tst = train_test_split(X, y, test_size=0.4)

    # create a SVM using the ovr type seperator
    clf = svm.LinearSVC()
    # train SVM with test split data
    clf.fit(X_trn, y_trn)
    # test SVM with the x test data set
    print("test predictions: ", clf.predict(X_tst))
    # score with the y test data set
    print("test scores: ", clf.score(X_tst, y_tst))

    # seperate method for cross validation
    # cv_results = cross_validate(clf, X_tst, y_tst, return_train_score=False)
    # print(sorted(cv_results.keys()))                         
    # print(cv_results['test_score'])   
