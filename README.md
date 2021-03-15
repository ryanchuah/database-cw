# COMP00222 Databases and Information Systems  
## Group 3 Coursework

## To run:
1. In your terminal, navigate to root directory then do  
```
$ docker-compose up --build --scale server=n where n is the number of instances 
```
2. To test the server and database, enter `http://localhost/` into your browser. You should see an object of `favorite_colors`  
3. To test the client, open index.html in your browser. You should see a list of users and their colors.  

## To stop:
1. In another terminal, navigate to root directory then do 
```
$ docker-compose down
```

## Schema:
![ERD Diagram](https://github.com/ryanchuah/database-cw/tree/main/imgs/erd.png?raw=true)  
Above is the entity relationship diagram for our system. As you can see it consists of 9 tables. The left section of the ERD is for use cases 1-5 and the right section is for use case 6. Crow's feet notation is used in our ERD where a 3 pronged ending indicates a multiplicity of many and a dash ending indicates a multiplicity of 1. The majority of information pertaining to movies is stored in the movies table. Genres is its own separate table since it is a multi-valued attribute of movies. The same reason is why actors, ratings and tags also have their own separate tables that all relate to the movies table. There is also a users table and since any one user may provide multiple tags or ratings, there is a 1 to many relationship between the users table and the tags and ratings tables. The right side of the ERD consists of a table containing the personality details for each user and a table of predicted ratings based on the personality data. There is a 1 to many relationship between the user personality details and the personality ratings tables.

## Use cases/functions:
#### 1. Browsing films in the database (i.e., visual listings of films in the dataset, with user-modifiable views).
    Users can browse through the films in the database on the dedicated movies page. 
    The movies can be sorted by the title, popularity, polarity, average rating.
    Pagination allows the user to choose how many movies they'd like to view on the page.
#### 2. Searching for a film to obtain a report on viewer reaction to it (i.e., an interpreted report with aggregate viewer ratings, etc.).
    There is a navigation bar on the top of each of the webpages with an integrated search bar. The user can search by 
    the movie's title which will return a list of movies with the given word/phrase in its title.
    On the results page each movie listed hyperlinks to an individual page for that movie which has all the information 
    about the chosen movie. On the individual movie page the user will be able to see the movie's title, average rating,
    release year, poster, actors and genres. There is also a pie chart showing the percentage of users who gave the movie
    each rating. We also have a line graph showing the ratings for the movie within the first year of release.
#### 3. Reporting which are the most popular movies and which are the most polarising (extreme difference in ratings).
    The top 10 most popular and most polarising movies can be seen on the index page. Popularity and polarity were also 
    used as sort by options for the movies page.
#### 4. Segmenting the audience for a released movie (i.e., identifying categories of viewer by the rating and tag data, also in relation to data for ratings to all movies).
    Upon taking in the movie id, this query uses the available information for the movie to determine what percentage of 
    the users would also like other genres in the database. This information is displayed on the individual movie's page.
    The query finds all the users that have rated the movie > 3 then uses the tags they've inputed to see what other 
    genres users who like this movie may also like by returning the percentage of users that have also rated movies of 
    those genres highly. As an extension to that we also used the genres of the movies in the database to see what other
     genres people who like those genres also like.
#### 5. Predicting the likely viewer ratings for a soon-to-be-released film based on the tags and or ratings for the film provided by a preview panel of viewers drawn from the population of viewers in the database.
    On the frontend the marketing professionals is presented with a table to enter: the userID, ratings and/or tags. 
    The ratings' and/or tags' fields can be left blank if the marketing professional doesn't have the information for 
    the users from the preview panel. This query involved four main steps:
        1) For each user their tags are used to calculate the average rating of all the movies with the tags that the 
            user had assigned to the soon-to-be-released film.
        2) For each user the rating they assigned to this soon-to-be-released film was used to find all the other movies 
            that that specific had rated +/- 0.1 of the assigned rating for this film. Using the movieIds of all the 
            chosen movies the true average rating of those movies was caluclated. The average of the average ratings of 
            each of those movies was then used to get an approximate rating based on the user's inputed rating for this 
            soon-to-be-released film.
        3) The average rating of all the users in the preview panel were averaged.
        4) The three values calculated in the steps above were then averaged to calculate composite predicted rating 
            based on the tags and/or ratings from the preview panel.

    The assumptions made in this use case were:
        - The soon-to-be-released film does not exist in the database.
        - Information regarding the tags and/or ratings to be used for this use-case should be collected from the front-end,
        - The size of the preview panel isn't constant.
     
#### 6. Predicting the personality traits of viewers who will give a high rating to a soon-to-be-released film (using the personality/ratings dataset from GroupLens) whose tags are known.
    This use-case made use of the personality traits dataset from GroupLens. The query gets all movieIds from the original dataset that have the same tags as the soon-to-be released movie. From the personality dataset. we filter out users that have rated these movies less than 4.5 and average the personality traits of the remaining users.


## Additional Features:
### Load Balancing  
We also implemented a load balancer using Nginx to optimise resource utilisation, maximise throughput, and reduce latency across the multiple application instances. We implemented load balancing using round robin distribution due to its simplicity. It receives client requests and distributes them across servers in a repeated pattern, e.g. server A, server B, server C, server A etc. This ont only improves user experience but allows for the system to be scaled up and handle more requests and data in the future.  

### TMDB API

### Caching

## Assumptions


## Sample Request:
### Use case 1 & 3:
    (movies page URL)

### Use case 2:








## Viewing console output from index.js
1. Open index.html in Chrome
2. Open developer mode (for me it's Ctrl+f12)
3. Navigate to _console_
4. Refresh the page
    
