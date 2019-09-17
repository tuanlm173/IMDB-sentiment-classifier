import requests
from bs4 import BeautifulSoup
import urllib.parse
import json


# TODO: Get list of 2019 movies from imdb (tech: BeautifulSoup) => DONE (movie_imdb.py)

# TODO: Use API to search for imdb id for each movie (tech: IMDB API) => DONE (movie_imdb.py)
# try to remove all movies that have 0 reviews

# TODO: Get all user review for each film (tech: scrapy) => DONE (spider_imdb.py)

# TODO: perform sentiment analysis and classification of negative/positive based on reviews (tech: numpy, pandas, matplotlib, nltk, sklearn)


# Get list of movies
headers = {
    "Accept-Language": "en-US, en;q=1"
}  # refer to: https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4
LIST_MOVIES_URL = "https://www.imdb.com/list/ls071285512/"
r = requests.get(LIST_MOVIES_URL, headers=headers)
r_content = r.text

soup = BeautifulSoup(r_content, "html5lib")
items = soup.find("div", {"class": "lister-list"})
item_movies = items.find_all("h3")
list_movies = []
for i in item_movies:
    movie = i.find("a").text
    list_movies.append(movie)


# Get imdb id by Search API
params = {"page": 1, "r": "json"}
list_imdb_ids = []
for movie in list_movies:
    movie_encoded = urllib.parse.quote_plus(movie)
    IMDB_ID_URL = (
        "https://movie-database-imdb-alternative.p.rapidapi.com/"
        + "?"
        + urllib.parse.urlencode(params)
        + "&s="
        + movie_encoded
    )
    try:
        print("Getting IMDB id of: " + movie)
        r = requests.get(
            IMDB_ID_URL,
            headers={
                "X-RapidAPI-Host": "movie-database-imdb-alternative.p.rapidapi.com",
                "X-RapidAPI-Key": "f6e5204c15mshcb23d8ee2fe4ebep111d89jsn2958e632fb30",
            },
        )
        imdb_id = r.json()["Search"][0]["imdbID"]
        list_imdb_ids.append(imdb_id)
    except:
        list_imdb_ids.append("Not found")
results = dict(zip(list_movies, list_imdb_ids))
print(results)


RATING_URL = "https://www.imdb.com/title/{}/reviews?ref_=tt_urv"
lst_rating_url = []
for k, v in results.items():
    if v != "Not found":
        lst_rating_url.append(RATING_URL.format(v))
print(lst_rating_url)


file_name = "list_movies_imdbIDs.json"
with open(file_name, "w") as fp:
    json.dump(results, fp)

# r = requests.get("https://movie-database-imdb-alternative.p.rapidapi.com/?i=tt4154796&r=json&y=2019",
#  headers={
#    "X-RapidAPI-Host": "movie-database-imdb-alternative.p.rapidapi.com",
#    "X-RapidAPI-Key": "f6e5204c15mshcb23d8ee2fe4ebep111d89jsn2958e632fb30"
#  }
# )
