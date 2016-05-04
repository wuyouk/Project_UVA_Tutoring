from pyspark import SparkContext

import itertools

sc = SparkContext("spark://sparkMaster:7077", "PopularItems")
data = sc.textFile("/tmp/data/access.log")

# 1. Read data in as pairs of (user_id, item_id clicked on by the user)
pairs = data.map(lambda line: tuple(line.split("\t")))
# 1. pairs: ('1', '3')
# 1. Output example: ('1', '3')
# Discard multiple click results for a user
pairs = pairs.distinct()
output = sorted(pairs.collect())
for pair in output:
	print(pair)

print ("Print (user, item) pairs done")


# 2. Group data into (user_id, list of item ids they clicked on)
def s(x): return sorted(x)
# Make sure item id are sorted after groupByKey
user_items = pairs.groupByKey().mapValues(s)
# 2. user_items: ('1', <pyspark.resultiterable.ResultIterable object at 0x7f39563fe668>)
# 2. Output example: 1: 3, 333, 33, 33, 81, 
output = sorted(user_items.collect())
for user, items in output:
	print("("+user+": ", end='')
	first = True
	for item in items:
		if first == True:
			first = False
		else:
			print(", ", end='')
		print(item, end='')
	print(")")

print ("Print (user, items) pairs done")


# 3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
user_pair = user_items.flatMap(lambda ui: [(ui[0], pair) for pair in list(itertools.combinations(ui[1],2))])
# 3. user_pair: (1, ('333', '33'))
# 3. Output example: 1: ('333', '33')
output = sorted(user_pair.collect())
for user, pair in output:
	print("("+user+": "+str(pair)+")")

print ("Print (user, item_pair) pairs done")


# 4. Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2) 
pair_user = user_pair.map(lambda user_item: (user_item[1],user_item[0]))
# 4. pair_user: (('12', '3'), 2)
# 4. Output example: ('12', '3'): 2
output = sorted(pair_user.collect())
for pair, user in output:
	print("("+str(pair)+": "+user+")")

print ("Print (item_pair, users) pairs done")


# 5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
item_pair = pair_user.map(lambda pair: (pair[0], 1))
pair_count = item_pair.reduceByKey(lambda x,y: x+y)
# 5. pair_count: (('12', '3'), 1)
# 5. Output example: ('12', '3'): 1
output = sorted(pair_count.collect())
for pair, count in output:
	print("("+str(pair)+": "+str(count)+")")

print ("Print (item_pair, count) pairs done")


# 6. Filter out any results where less than 3 users co-clicked the same pair of items
pattern_pair = pair_count.filter(lambda pair: pair[1] >= 3)
# 6. pair_count: (('3', '33'), 3)
# 6. Output example: ('3', '33'): 3
output = sorted(pattern_pair.collect())
for pair, count in output:
	print("("+str(pair)+": "+str(count)+")")

print ("Print (pattern_pair, count) pairs done")