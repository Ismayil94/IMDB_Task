#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests


def get_year(url):
    """Gets data from [url] by the help of BeautifulSoup4 and gets movie years
    Arguments:
       - url -- url of the page that we want parse from
    Returns:
        - data -- list of movie release years
    """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')

    data = []
    movies = soup.find('tbody', class_='lister-list').find_all('tr')
    for movie in movies:
        data.append(movie.find('span', class_='secondaryInfo').text)
    requests.session().close()
    return data


def get_data(url):
    """Gets data from [url] by the help of BeautifulSoup4 and gets movie data
    Arguments:
       - url -- url of the page that we want parse from
    Returns:
        - data -- list of movie data with dictionary of movies 
    """
    # url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250_6'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')

    data = []
    movies = soup.find('tbody', class_='lister-list').find_all('tr')

    for movie in movies:
        item = {}
        item['title'] = movie.find('td', class_='titleColumn').text
        item['year'] = movie.find('span', class_='secondaryInfo').text
        item['rating'] = movie.find('td', class_='imdbRating').strong.text
        data.append(item)
    requests.session().close()
    return data

if __name__ == "__main__":
    print("Not for running it!!!")