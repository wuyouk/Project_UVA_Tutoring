import random
import sys


target = open("access2.log", 'a')
for i in range(30):
	l = str(random.randrange(0, 10))+"\t"+str(random.randrange(0, 10))
	target.write(l)
	target.write("\n")

target.close()