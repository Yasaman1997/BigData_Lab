from math import sqrt
from numpy import *
from numpy import linalg as la
import numpy as np
import math

# we tried both methods 

# ----------------------------------------------#	
# ---------------input type: dict---------------#
# ----------------------------------------------#	

def sim_pearson(prefs, p1, p2):
    # get list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
            
    # find the number of elements
    n = len(si)
    
    # if they are no ratings in common, return 0
    if n == 0: return 0
    
    # add up all the preferences:
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    
    # sum up the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    
    # sum up the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    
    # calculate pearson score
    num = pSum - ((sum1 * sum2)/n)
    den = sqrt((sum1Sq - pow(sum1, 2)/n) * (sum2Sq - pow(sum2, 2)/n))
    if den == 0: return 0
    
    r = num/den
    return r
    
def similarUsers(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    # sort the list
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecommendations(prefs, person, similarity = sim_pearson):
	totals = {}
	simSums = {}
	for other in prefs:
		# exclude self
		if other == person: continue
		
		sim = similarity(prefs, person, other)
		
		# ignore scores of zero or lower
		if sim <= 0: continue
		
		for item in prefs[other]:
			
			# only score movies the person has not yet seen
			if item not in prefs[person] or prefs[person][item] == 0:
				totals.setdefault(item, 0.)
				totals[item] += prefs[other][item]*sim
				# sum of sim
				simSums.setdefault(item, 0.)
				simSums[item] += sim
		# create normalized list
		rankings = [(total/simSums[item], item) for item, total in totals.items()]
		
		# sort the list
		rankings.sort()
		rankings.reverse()
		return rankings
	
# ----------------------------------------------#	
# ---------------input type: numpy--------------#
# ----------------------------------------------#
	
def getcorrelation(dat, u1, u2):
	test1 = np.nonzero(dat[u1])[0]
	test2 = np.nonzero(dat[u2])[0]
	
	# find overlap indices
	items = []
	for i in test1:
		if i in test2:
			items.append(i)
	if len(items) == 0: return 0
	
	# calculate correlations on items that are mutually rated
	to_calc_1 = np.array(dat[0][items])
	to_calc_2 = np.array(dat[1][items])

	correlation = np.corrcoef(to_calc_1, to_calc_2)[0][1] # returns only a number
	
	if math.isnan(correlation): return 0
	
	return correlation

def findsimusers(dat, user, n = 5, similarity=getcorrelation):
	scores = []
	for other in range(len(dat)):
		if other != user-1:
			scores.append([similarity(dat, user-1, other), other])
	# sort the list
	scores.sort()
	scores.reverse()
	
	return scores[:n]

def getmemovies(dat, user, movies, n=5, similarity=getcorrelation):
	
	to_rec = []
	
	for other in range(len(dat)):
		if other == user-1: continue
		sim = similarity(dat, user-1, other)
	 	if sim <= 0: continue
	 	for item in np.where(dat[other] != 0)[0]:
	 		if item not in np.nonzero(dat[user])[0] or dat[user][item] == 0:
	 			item_rating = dat[other][item]*sim
	 			temp = [item_rating, item]
				to_rec.append(temp)
	# sort
	to_rec.sort()
	to_rec.reverse()
	movie_rec = []
	
	for i in range(n):
		name = movies[to_rec[i][1]]
		movie_rec.append(name)
	
	return movie_rec

def cv_user(dat, test_ratio, similarity = getcorrelation):
	number_of_users = np.shape(dat)[0]
	user_list = np.array(range(0, number_of_users))
	test_user_size = test_ratio*number_of_users
	test_user_indices = np.random.randint(0, number_of_users, test_user_size)
	witheld_users = user_list[test_user_indices]

	maes = 0
	
	for user in witheld_users:
		number_of_items = np.shape(dat)[1]
		rated_items_by_user = np.array(np.nonzero(dat[user])[0])
		test_size = test_ratio * len(rated_items_by_user)
		test_indices = np.random.randint(0, len(rated_items_by_user), test_size)
		witheld_items = rated_items_by_user[test_indices]
		original_user_profile = np.copy(dat[user])
		dat[user, witheld_items] = 0 # set to 0
		
		error_u = 0
		count_u = len(witheld_items)

		simuser = findsimusers(dat, user, n=1)[0][1]
		to_test = []
		sim = similarity(dat, user, simuser)
		
		for item in np.where(dat[simuser]!= 0)[0]:
	 		if item not in np.nonzero(dat[user])[0] or dat[user][item] == 0:
	 			item_rating = dat[simuser][item]*sim
	 			temp = [item_rating, item]
				to_test.append(temp)
		
		for i in to_test:
			item_name = i[1]
			item_pred_rating = i[0]
			err = abs(dat[user][item_name] - item_pred_rating)
			error_u += err
			temp_ames = error_u/count_u
			maes += temp_ames

	MAE = maes/len(witheld_users)
	
	print "The MAE  is for user-based collaborative filtering is: %0.5f" % MAE
	
	return MAE
			

	
	
	
	
	
	

	
	
	
	
	
	
	
	
	
	
		
	
		
		
		
		
		
		
		
	












	
