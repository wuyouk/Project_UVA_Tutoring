# Project4501_spark

Shin, Byung Eun / Cronk, Michael / Wu, You

bs5sk@Virginia.EDU, mpc3ea@Virginia.EDU, yw5g@Virginia.EDU

In this project, we build a map/reduce job on Apache Spark, which takes a web site access log as input and as output produce data that can be used by a recommendation system.

Run the following commands to start the map/reduce job:

```
docker-compose up
```

```
docker exec -it project4501spark_sparkWorker_1 bin/spark-submit --master spark://sparkMaster:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/driver.py
```

* [driver.py](https://github.com/Mcronk/project4501_spark/blob/master/driver.py) is the driver program and completes the following six steps. (By default using *access.log* as input) 

  **Note:** For grading purpose, the values of RDD after each step is printed. For final production use, please comment RDD.collect process after step 1 to step 5.
  1. Read data in as pairs of (user_id, item_id clicked on by the user)
  
    ('1', '3')
('1', '33')
('1', '333')
('1', '81')
('11', '6')
('11', '66')
('11', '666')
('12', '6')
('12', '66')
('12', '666')
('13', '6')
('13', '66')
('13', '666')
('18', '6')
('18', '66')
('18', '666')
('19', '6')
('19', '66')
('19', '666')
('2', '12')
('2', '3')
('2', '32')
('2', '33')
('2', '333')
('3', '13')
('3', '3')
('3', '33')
('3', '333')
('3', '93')

  2. Group data into (user_id, list of item ids they clicked on)
  
    (1: 3, 33, 333, 81)
(11: 6, 66, 666)
(12: 6, 66, 666)
(13: 6, 66, 666)
(18: 6, 66, 666)
(19: 6, 66, 666)
(2: 12, 3, 32, 33, 333)
(3: 13, 3, 33, 333, 93)

  3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
  
    (1: ('3', '33'))
(1: ('3', '333'))
(1: ('3', '81'))
(1: ('33', '333'))
(1: ('33', '81'))
(1: ('333', '81'))
(11: ('6', '66'))
(11: ('6', '666'))
(11: ('66', '666'))
(12: ('6', '66'))
(12: ('6', '666'))
(12: ('66', '666'))
(13: ('6', '66'))
(13: ('6', '666'))
(13: ('66', '666'))
(18: ('6', '66'))
(18: ('6', '666'))
(18: ('66', '666'))
(19: ('6', '66'))
(19: ('6', '666'))
(19: ('66', '666'))
(2: ('12', '3'))
(2: ('12', '32'))
(2: ('12', '33'))
(2: ('12', '333'))
(2: ('3', '32'))
(2: ('3', '33'))
(2: ('3', '333'))
(2: ('32', '33'))
(2: ('32', '333'))
(2: ('33', '333'))
(3: ('13', '3'))
(3: ('13', '33'))
(3: ('13', '333'))
(3: ('13', '93'))
(3: ('3', '33'))
(3: ('3', '333'))
(3: ('3', '93'))
(3: ('33', '333'))
(3: ('33', '93'))
(3: ('333', '93'))

  4. Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2) 
  
    (('12', '3'): 2)
(('12', '32'): 2)
(('12', '33'): 2)
(('12', '333'): 2)
(('13', '3'): 3)
(('13', '33'): 3)
(('13', '333'): 3)
(('13', '93'): 3)
(('3', '32'): 2)
(('3', '33'): 1)
(('3', '33'): 2)
(('3', '33'): 3)
(('3', '333'): 1)
(('3', '333'): 2)
(('3', '333'): 3)
(('3', '81'): 1)
(('3', '93'): 3)
(('32', '33'): 2)
(('32', '333'): 2)
(('33', '333'): 1)
(('33', '333'): 2)
(('33', '333'): 3)
(('33', '81'): 1)
(('33', '93'): 3)
(('333', '81'): 1)
(('333', '93'): 3)
(('6', '66'): 11)
(('6', '66'): 12)
(('6', '66'): 13)
(('6', '66'): 18)
(('6', '66'): 19)
(('6', '666'): 11)
(('6', '666'): 12)
(('6', '666'): 13)
(('6', '666'): 18)
(('6', '666'): 19)
(('66', '666'): 11)
(('66', '666'): 12)
(('66', '666'): 13)
(('66', '666'): 18)
(('66', '666'): 19)

  5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
  
    (('12', '3'): 1)
(('12', '32'): 1)
(('12', '33'): 1)
(('12', '333'): 1)
(('13', '3'): 1)
(('13', '33'): 1)
(('13', '333'): 1)
(('13', '93'): 1)
(('3', '32'): 1)
(('3', '33'): 3)
(('3', '333'): 3)
(('3', '81'): 1)
(('3', '93'): 1)
(('32', '33'): 1)
(('32', '333'): 1)
(('33', '333'): 3)
(('33', '81'): 1)
(('33', '93'): 1)
(('333', '81'): 1)
(('333', '93'): 1)
(('6', '66'): 5)
(('6', '666'): 5)
(('66', '666'): 5)

  6. Filter out any results where less than 3 users co-clicked the same pair of items
  
    (('3', '33'): 3)
(('3', '333'): 3)
(('33', '333'): 3)
(('6', '66'): 5)
(('6', '666'): 5)
(('66', '666'): 5)
  
* [random_generator.py](https://github.com/Mcronk/project4501_spark/blob/master/random_generator.py) generates 30 more arbitrary logs to *access2.log* after running ```python random_generator.py```.

* [access.log](https://github.com/Mcronk/project4501_spark/blob/master/access.log) and [access2.log](https://github.com/Mcronk/project4501_spark/blob/master/access2.log) are the sample input files and has a format of ```userID \t itemID``` as each line.



