# database-cw  
I'm doing my best

## To run:
1. In your terminal, navigate to root directory then do  
```
$ docker-compose up
```
2. To test the server and database, enter `http://0.0.0.0:5000/` into your browser. You should see an object of `favorite_colors`  
3. To test the client, open index.html in your browser. You should see a list of users and their colors.  

## To stop:
1. In another terminal, navigate to root directory then do 
```
$ docker-compose down
```

## Viewing console output from index.js
1. Open index.html in Chrome
2. Open developer mode (for me it's Ctrl+f12)
3. Navigate to _console_
4. Refresh the page
    