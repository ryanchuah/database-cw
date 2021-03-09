# OUTDATED. IGNORE THIS

/movies

### Query Params

-   **sortBy**: ['column', 'popularity', 'polarity']
-   **limit**: int > 1
-   **page**: int > 1
-   **column** _(optional)_: column name of Movies table to sort by. Only required if **sortBy**=column

### Example

`http://localhost:5000/movies?limit=10&sortBy=popularity&page=1`

### Returns

```
{
    "movies": [
        {
            "movieId": 318,
            "title": "Shawshank Redemption, The ",
            "release_year": 1994,
            "votes": 317,
            "avg_ratings": 4.429022082018927
        },
        ...,
    ]
}
```
