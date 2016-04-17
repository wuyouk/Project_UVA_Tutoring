#Group 3 Project:

The project is about building a tutoring platform that connects students who needs tutoring and tutors who have talents in certain subjects and wants to offer classes. 

Shin, Byung Eun / Cronk, Michael / Wu, You

bs5sk@Virginia.EDU, mpc3ea@Virginia.EDU, yw5g@Virginia.EDU

<br>

###Project 6###

Four improvements are done in this iteration.

1. Hosting on DigitalOcean (Cronk, Michael)
  * Digital Ocean Link:  http://159.203.160.81:8000
2. Integration tests (Shin, Byung Eun)
  * Download [project4501_test](https://github.com/Mcronk/project4501_test/releases) and run ```python test.py```
  * Selenium was used to create integration tests for the web front-end. These tests were used to simulate these five different actions that users could take:
    * Make a search query
    * Sign up for the website
    * Create a tutoring posting while logged in
    * Create a tutoring posting while logged out
    * Log in
  * The front-end passed all of these tests but it would be useful in the future to run these tests again after making changes to the API or web layers. The result of the tests are shown below.
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/integration_test.png)
3. Performance testing (Wu, You)
  * Download [project4501_test](https://github.com/Mcronk/project4501_test/releases). If use non-GUI mode, run ```jmeter -n -t <path>/ThreadGroup.jmx```, otherwise, open *ThreadGroup.jmx* with installed JMETER.
  * Use Jmeter, by setting different number of threads and ramp-up period, the following GET and POST request sequence is carried out.
    * GET1: Visit home, courses, course-1, course-2, course-3 pages in a row. Threads = 50, period = 10.
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/GET-50-10.png)
      * Latency mainly comes from Courses Page. There are 393 courses in the database and obviously collecting these courses’ information takes a lot of time.
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/393%20courses.png)
      * GET2: Visit home, course-1, course-2, course-3 pages in a row (No courses request this time). Threads = 100, period = 10.
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/GET2-100-10.png)
      * It is much faster this time. Increasing the load slows down the response time. See below for Threads = 150, period = 10 and Threads = 200, period = 10 samples.
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/GET2-150-10.png)
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/GET2-200-10.png)
      * POST1: Visit home, sign up, log in, create course, search, log out. See below for Threads = 20, period = 10 and Threads = 30, period = 10 samples. 
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/POST-20-10.png)
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/POST-30-10.png)
      * It is much slower for POST requests than GET requests. Among the requests, Search seems takes the greatest time. So let’s do the following requests without Search.
      * POST2: Visit home, sign up, log in, create course, log out. See below for Threads = 30, period = 10, Threads = 50, period = 10 and Threads = 80, period = 10  samples. 
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/POST2-30-10.png)
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/POST2-50-10.png)
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/POST2-80-10.png)
      * Latency becomes a problem (average 1s for Login and 3s for Create course) until we increase load to 8 threads per second. (3 threads per sec and 5 threads per sec are fine)
      * Performance graphs provided by DigitalOcean
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/do_bandwidth.png)
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/do_cpu.png)
![alt tag](https://github.com/Mcronk/project4501_test/blob/master/screenshot_test/do_disk.png)
4. Load balancing (Cronk, Michael and Wu, You)
  * Use [Pen] (https://hub.docker.com/r/galexrt/pen/) as the load balancer in front of *WEB* layer.
  * After ```docker-compose up```, run ```docker-compose scale web=3``` and ```docker run -d --name pen -p 8000:8000 --link compose_web_1:compose_web_1 --link compose_web_2:compose_web_2 --link compose_web_3:compose_web_3 galexrt/pen:latest -r 8000 compose_web_1:8000 compose_web_2:8000 compose_web_3:8000```. Number of scaling is up to change.
  * In the home page, small header under the “GitHub” button displays the container ID. Refreshing will cause Pen to switch which container the request is sent to.  This will change the displayed container ID.  

The above description can also be viewed in the Google Doc [write up](https://docs.google.com/a/virginia.edu/document/d/14VVxMV0ZZ5zEVFEPpaYQqixSamFwxQqzfXEdTXcKx88/edit?usp=sharing).

Please download the following releases, change the volume path in *docker-compose.yml* to match local setting, then ```docker-compose up```.

1. [project4501_web](https://github.com/Mcronk/project4501_web/releases)
2. [project4501_exp](https://github.com/Mcronk/project4501_exp/releases)
3. [project4501_models](https://github.com/Mcronk/project4501_models/releases)
4. [project4501_batch](https://github.com/Mcronk/project4501_batch/releases)
5. [project4501_test](https://github.com/Mcronk/project4501_test/releases)
6. [Compose](https://github.com/Mcronk/project4501_compose/releases)

*Note: models, exp and batch are the same since last interation and the default volume setting uses the downloaded repo name:* \<name\>-master

<br>

###Project 5###

Please download the following releases, change the volume path in *docker-compose.yml* to match local setting, then ```docker-compose up```.

1. [project4501_web](https://github.com/Mcronk/project4501_web/releases)
2. [project4501_exp](https://github.com/Mcronk/project4501_exp/releases)
3. [project4501_models](https://github.com/Mcronk/project4501_models/releases)
4. [project4501_batch](https://github.com/Mcronk/project4501_batch/releases)
5. [Compose](https://github.com/Mcronk/project4501_compose/releases)

*Note: the default volume setting uses the downloaded repo name:* \<name\>-master

<br>
**Project Flow**:

1. Visit <[Home page](http://localhost:8000)>
  * User can use the SEARCH bar on each page to search for desired courses
  * Search key words include course name, tag, description, available time, price, qualification
2. Create Course <[Listing page](http://localhost:8000/listing/)>
  * Create a new course, new course would be indexed
  * Start a new search, newly added course would be displayed if query matches
 
<br>

###Project 4###

Please download the following releases, change the volume path in *docker-compose.yml* to match local setting, then ```docker-compose up```.

1. [project4501_web](https://github.com/Mcronk/project4501_web/releases)
2. [project4501_exp](https://github.com/Mcronk/project4501_exp/releases)
3. [project4501_models](https://github.com/Mcronk/project4501_models/releases)
4. [Compose](https://github.com/Mcronk/project4501_compose/releases)

*Note: the default volume setting uses the downloaded repo name:* \<name\>-master

<br>
**Project Flow**:

1. Visit <[Home page](http://localhost:8000)>
  * User can access all functionalities of this project through buttons on upper-right corner
  * Login can only be used after logout, vice versa
2. Signup <[Signup page](http://localhost:8000/signup/)>
  * Errow msg would display if email has been registered
  * If no user has login, after signup, user would be directed to <Login page>
  * If a user has login, after signup, user would go back to <Home page>
3. Login <[Login page](http://localhost:8000/login/)>
  * Use email and password to login
  * Error msg would display if user does not exist or wrong password
4. Create Course <[Listing page](http://localhost:8000/listing/)>
  * If user is not logged in, user would be directed to <Login page>
  * After successfully created course, user would be directed to newly added course info page <Course page>
5. Logout <[Logout page](http://localhost:8000/logout/)>
  * Logout deletes authenticator cookie

<br>

###Project 3###

```
git clone https://github.com/Mcronk/project4501_compose.git
docker-compose up
```

Set up three layers:

1. [project4501_web](https://github.com/Mcronk/project4501_web)
2. [project4501_exp](https://github.com/Mcronk/project4501_exp)
3. [project4501_models](https://github.com/Mcronk/project4501_models)

Three sites up:

1. [Home page](http://localhost:8000)
2. [Courses page](http://localhost:8000/courses/)
3. [Course page](http://localhost:8000/course/1)

**About** and **Courses** in [Home page](http://localhost:8000) and [Course page](http://localhost:8000/course/1) are clickable active *href*. 

**Course title** in [Courses page](http://localhost:8000/courses/) is active *href*. 
