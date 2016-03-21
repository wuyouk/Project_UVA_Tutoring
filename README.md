#Group 3 Project:

The project is about building a tutoring platform that connects students who needs tutoring and tutors who have talents in certain subjects and wants to offer classes. 

Shin, Byung Eun / Cronk, Michael / Wu, You

bs5sk@Virginia.EDU, mpc3ea@Virginia.EDU, yw5g@Virginia.EDU

<br>

###Project 4###

Please download the following releases, change the volume path in **docker-compose.yml** to match local setting, then **docker-compose up**.

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
