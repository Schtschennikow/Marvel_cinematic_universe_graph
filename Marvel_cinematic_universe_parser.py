import requests
from bs4 import BeautifulSoup as soup
import re
from collections import defaultdict as dd
import re
import pandas as pd
from collections import Counter

def main():
    r = requests.get('https://www.imdb.com/list/ls026723944/').text
    data = soup(r, 'lxml')
    data_list = data.find_all("div", {"class":"list-description"})
    data_json = {}

    for dl in data_list[1:]:
        char = dl.find('p').text.strip()
        films = [re.sub(r' \(\d{4}\)', '', s.text) for s in dl.find_all('li')]
        if not char in data_json:
            data_json[char] = films
        else:
            data_json[char].extend(films)

    films_set = set()
    for char, films in data_json.items():
        films_set.update(films)

    marvel_data_json = dd(list)
    for film in films_set:
        for char, films in data_json.items():
            if film in films:
                marvel_data_json[film].append(re.sub(r'/ .+',  '', char))

    wunderbar = []
    for film, chars in marvel_data_json.items():
        for i, char in enumerate(chars):
            for c in chars[i+1:]:
                t = (char, "Undirected", c)
                wunderbar.append(t)

    wunderbar_marvel = []
    for t in wunderbar:
        rev_t = (t[2], t[0])
        if not t in wunderbar_marvel or not rev_t in wunderbar_marvel:
            wunderbar_marvel.append(t)

    wow = Counter(wunderbar_marvel).most_common()
    big_wunderbar_marvel = []
    for ttt in wow:
        lll = list(ttt[0])
        lll.append(ttt[1])
        big_wunderbar_marvel.append(lll)
    columns=["Source", "Type", "Target", "Weight"]
    pd.DataFrame(big_wunderbar_marvel, 
                 columns=columns).to_csv("Marvel_cinematic_universe.csv", 
                                                               index=False)
main()