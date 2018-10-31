# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 19:50:06 2018

@author: Francesco
"""
import numpy as np


critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0}, 
         'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
         'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0}, 
         'Claudia Puig': {'Snakes on a Plane': 3.5,'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5}, 
         'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0}, 
         'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5}, 
         'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def sim_distance(prefs, person1, person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
        if len(si)==0:
            return 0
    sum_of_squares = sum(((prefs[person1][item] - prefs[person2][item])**2) for item in si)
    return 1/(1+(sum_of_squares**0.5))
def sim_pearson(prefs, person1, person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
        n = len(si)
        if n==0:
            return 0
    sum1 = sum((prefs[person1][item]) for item in si)
    print('sum1: ', sum1)
    sum2 = sum((prefs[person2][item]) for item in si)
    print('sum2: ', sum2)
    sum1sq = sum((prefs[person1][item]**2) for item in si)
    print('sum1sq: ', sum1sq)
    sum2sq = sum((prefs[person2][item]**2) for item in si)
    print('sum2sq: ', sum2sq)
    
    product_sum = sum((prefs[person1][item]*prefs[person2][item]) for item in si)
    print('product_sum:',product_sum)
    
    num = product_sum - (sum1*sum2/n)
    den = ((sum1sq - (sum1**2)/n)*(sum2sq - (sum2**2)/n))**0.5
    r = num/den
    if den == 0:
        return 0
    else:
        return r
    
def topMatches(prefs, person, n=5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]
#person1 = input("Person 1:")
#person2 = input("Person 2:")
print(topMatches(critics,'Toby', n=5))



