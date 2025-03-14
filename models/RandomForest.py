"""
Author      : Madison Hobbs
Class       : HMC CS 158
Date        : 2018 April 14
Description : Random Forest Tuning and Performance
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import validations
from sklearn.metrics import f1_score, make_scorer, accuracy_score, average_precision_score, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
# modify path because these files are in a different directory
import sys
sys.path.insert(0, '../data+wrangling')
import util

def tune(X_train, y_train, scoring):
    
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)] 
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]

    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

    fracNeg = len(y_train[y_train == 0])/float(len(y_train))
    weight = (1-fracNeg)/float(fracNeg) 
    class_weight = {1:1, 0:weight}

    rf = RandomForestClassifier(class_weight=class_weight, criterion="entropy")
    # automatically does stratified kfold
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 5, verbose=2, random_state=42, n_jobs = -1, scoring=scoring)
    rf_random.fit(X_train, y_train)
    return rf_random.best_params_, rf_random.best_score_
    

def main():
    X_train = pd.read_csv("X_train.csv").drop(['Unnamed: 0'], axis = 1)
    #X_train = X_train[['200', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210']]
    X_train = X_train.values
    print X_train.shape
    X_test = pd.read_csv("X_test.csv").drop(['Unnamed: 0'], axis = 1)
    #X_test = X_test[['200', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210']]
    X_test = X_test.values
    print X_test.shape
    y_train = pd.read_csv("y_train.csv")['0']
    y_train = y_train.values
    print y_train.shape
    y_test = pd.read_csv("y_test.csv")['0']
    y_test =  y_test.values
    print y_test.shape

    #colnames = ['num_comments', 'num_shares', 'num_likes', 'num_loves', 'num_wows', 'num_hahas', 'num_sads', 'num_angrys', 'Category_left', 'Category_mainstream', 'Category_right']
    colnames = [u'2016', u'actual', u'address', u'aid', u'alleg', u'also', u'america', u'american', u'among', u'back', u'bad', u'barack', u'battleground', u'berni', u'best', u'better', u'bill', u'black', u'board', u'break', u'bush', u'busi', u'bust', u'call', u'came', u'campaign', u'candid', u'carolina', u'caught', u'chariti', u'check', u'children', u'chris', u'christi', u'citi', u'claim', u'clinton', u'cnn', u'come', u'communiti', u'compani', u'controversi', u'countri', u'court', u'crime', u'crimin', u'crisi', u'critic', u'cruz', u'dead', u'debat', u'definit', u'direct', u'director', u'donald', u'done', u'drug', u'effort', u'email', u'employe', u'entir', u'event', u'evid', u'expos', u'fact', u'fast', u'father', u'fbi', u'first', u'florida', u'follow', u'foreign', u'former', u'foundat', u'fox', u'frisk', u'gari', u'georg', u'get', u'give', u'gop', u'gun', u'happen', u'hell', u'hide', u'hofstra', u'holt', u'huge', u'immigr', u'includ', u'interview', u'jill', u'johnson', u'kill', u'latest', u'leader', u'leav', u'lester', u'lie', u'littl', u'look', u'make', u'may', u'mayb', u'mean', u'mike', u'militari', u'million', u'minut', u'monday', u'morn', u'mouth', u'move', u'name', u'nation', u'new', u'night', u'nomine', u'north', u'offic', u'open', u'part', u'paul', u'pay', u'penc', u'person', u'point', u'polici', u'polit', u'poll', u'prais', u'prepar', u'presid', u'presidenti', u'pretti', u'privat', u'profil', u'public', u'question', u'rahami', u'receiv', u'record', u'refuge', u'rep', u'republican', u'respect', u'riot', u'run', u'russia', u'russian', u'ryan', u'said', u'sander', u'say', u'second', u'secretari', u'senat', u'set', u'shoot', u'show', u'sight', u'spend', u'stage', u'stand', u'start', u'state', u'stop', u'su', u'suggest', u'support', u'syrian', u'system', u'take', u'ted', u'televis', u'tell', u'terrifi', u'three', u'tie', u'tim', u'time', u'total', u'tri', u'trump', u'tweet', u'two', u'univers', u'video', u'vote', u'voter', u'want', u'war', u'week', u'win', u'women', u'wonder', u'work', u'wow', u'year', u'york', 'num_comments', 'num_shares', 'num_likes', 'num_loves', 'num_wows', 'num_hahas', 'num_sads', 'num_angrys', 'Category_left', 'Category_mainstream', 'Category_right']
    print len(colnames)

    fracNeg = len(y_train[y_train == 0])/float(len(y_train))
    print "fraction of data training examples which have negative response: " + str(fracNeg)
    fracPos = len(y_train[y_train == 1])/float(len(y_train))
    print "fraction of data training examples which have positive response: " + str(fracPos)
    # minority class gets larger weight (as per example in class)
    weight = (1-fracNeg)/float(fracNeg) 
    print "negative weight is: " + str(weight)
    class_weight = {1:1, 0:weight}

    # NOTE: Commented the Cross Validation out and saved the best model below # 
    ################################################################################### ##########################################
    # 5 fold cv
    #best_params, best_score = tune(X_train, y_train, 'f1_weighted')
    #print best_params
    #print best_score
    # 3 fold best for f1_weighted = {'bootstrap': True, 'min_samples_leaf': 1, 'n_estimators': 400, 
    # 'max_features': 'sqrt', 'min_samples_split': 5, 'max_depth': 30}
    #
    # {'bootstrap': True, 'min_samples_leaf': 2, 'n_estimators': 1000, 'max_features': 'auto', 
    # 'min_samples_split': 22, 'max_depth': 110}
    #
    # 5 fold best trained on entropy ones {'bootstrap': False, 'min_samples_leaf': 2, 'n_estimators': 1600, 
    # 'max_features': 'sqrt', 'min_samples_split': 27, 'max_depth': 80}
    # smaller search area : {'bootstrap': True, 'min_samples_leaf': 1, 'n_estimators': 400, 
    # 'max_features': 'sqrt', 'min_samples_split': 5, 'max_depth': 100}
    #
    # the one we're actually using because has right features:
    # {'bootstrap': True, 'min_samples_leaf': 1, 'n_estimators': 400, 'max_features': 'sqrt', 'min_samples_split': 5, 'max_depth': 100}
    ########################################################################################################
    # {'bootstrap': True, 'min_samples_leaf': 1, 'n_estimators': 2000, 'max_features': 'sqrt', 'min_samples_split': 5, 'max_depth': 100}
    # all - CV f1 0.871467618968
    rf_f1 = RandomForestClassifier(class_weight=class_weight, bootstrap = True, min_samples_leaf = 1, n_estimators =  2000, max_features = 'sqrt', min_samples_split = 5, max_depth = 100, criterion="entropy")
    
    # meta only
    # {'bootstrap': True, 'min_samples_leaf': 2, 'n_estimators': 600, 'max_features': 'auto', 'min_samples_split': 10, 'max_depth': 100}
    # rf_f1 = RandomForestClassifier(class_weight=class_weight, bootstrap = True, min_samples_leaf = 2, n_estimators =  600, max_features = 'auto', min_samples_split = 10, max_depth = 100, criterion="entropy")
    rf_f1.fit(X_train, y_train)
    preds = rf_f1.predict(X_train)
    print "train f1_score: " + str(f1_score(y_train, preds, average="weighted")) # 0.9958
    preds = rf_f1.predict(X_test)
    print "test f1_score: " + str(f1_score(y_test, preds, average="weighted")) # 0.88877
    print "confusion matrix trained with f1: \n" + str(confusion_matrix(y_test, preds))

    importances = rf_f1.feature_importances_
    std = np.std([tree.feature_importances_ for tree in rf_f1.estimators_],
             axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")

    #feats = []
    #imps = []
    for f in range(X_train.shape[1]):
        print("%d. %s (%f)" % (f + 1, colnames[indices[f]], importances[indices[f]]))
        #feats.append(colnames[indices[f]])
        #imps.append(importances[indices[f]])

    #validations.check_overfit(rf_f1, f1_score, "weighted")
    #validations.check_overfit(rf_f1, accuracy_score, "accuracy")

    # print tune(X_train, y_train, 'accuracy')
    # 3 fold best for accuracy: best is {'bootstrap': True, 'min_samples_leaf': 1, 'n_estimators': 200, 'max_features': 'sqrt', 'min_samples_split': 2, 'max_depth': 50}
    #rf_accuracy = RandomForestClassifier(class_weight=class_weight, bootstrap = True, min_samples_leaf = 1, n_estimators = 200, max_features = 'sqrt', min_samples_split = 2, max_depth = 50, criterion="entropy")
    rf_accuracy = rf_f1
    rf_accuracy.fit(X_train, y_train)
    preds = rf_accuracy.predict(X_train)
    print "train accuracy: " + str(accuracy_score(y_train,preds)) # 1.0
    preds = rf_accuracy.predict(X_test)
    print "test accuracy: " + str(accuracy_score(y_test, preds))
    print "confusion matrix trained with accuracy: \n" + str(confusion_matrix(y_test, preds)) #0.887
    
    #validations.check_overfit(rf_accuracy, accuracy_score)

    #print tune(X_train, y_train, 'average_precision')
    # 3 fold best for precision is {'bootstrap': False, 'min_samples_leaf': 1, 'n_estimators': 800, 'max_features': 'sqrt', 'min_samples_split': 5, 'max_depth': 90}
    #rf_precision = RandomForestClassifier(class_weight=class_weight, bootstrap = False, min_samples_leaf = 1, n_estimators = 800, max_features = 'sqrt', min_samples_split = 5, max_depth = 90, criterion="entropy")
    rf_precision = rf_f1
    rf_precision.fit(X_train, y_train)
    preds = rf_precision.predict(X_train)
    print "train precision: " + str(average_precision_score(y_train, preds)) # 0.9999
    preds = rf_precision.predict(X_test)
    print "test precision: " + str(average_precision_score(y_test, preds)) # 0.96h
    print "confusion matrix trained with precision: \n" + str(confusion_matrix(y_test, preds))