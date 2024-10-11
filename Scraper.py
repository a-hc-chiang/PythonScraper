import requests
from bs4 import BeautifulSoup
import csv 
import time

def scrape_mal(anime_url):
    response = requests.get(anime_url)
    
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return []
    soup = BeautifulSoup(response.content, 'html.parser')
    res = []

    title = soup.find('span', {"itemprop": "name"}) 
    res.append(title.text.strip())

    authors = []
    author = soup.find('span', {"class": "author"})  # Access the first child element properly
    children = author.find_all("a")  # Find the first tag inside the author span
    for i in children:
        authors.append(i.text.strip())
    res.append(str(authors))

    genresList = []
    genres = soup.find_all('span', {"itemprop": "genre"})
    for genre in genres:
        genresList.append(genre.text.strip())
    
    try:
        demographic = soup.find('span', string="Demographic:").next_sibling.text.strip()
        genresList.append(demographic)
        res.append(str(genresList))
    except: 
        res.append("N/A")

    coverImage = soup.find('img', {"itemprop": "image"})
    res.append(coverImage.get('data-src'))

    seriesType = soup.find('span', string='Type:').find_next('a').text.strip()
    res.append(seriesType)

    seriesStatus = soup.find('span', string="Status:").next_sibling.text.strip()
    res.append(seriesStatus)

    publishDate = soup.find('span', string="Published:").next_sibling.text.strip()
    res.append(publishDate)

    summary = soup.find('span', {'itemprop':'description'})
    res.append(summary)

    return res

# title: idx 0, authors: idx 1, genres: idx 2, cover image: idx 3, 
# series type: idx 4, series status idx 5, publish date: idx 6, summary: idx 7, seriesID: idx 8 
# last scraped id: 1091
# curr val 3669 166659

anime_url = "https://myanimelist.net/manga/"
with open ('test.csv','a', newline='') as my_file:
    csv_writer = csv.writer(my_file)
    #headers for csv file 
    #csv_writer.writerow(['title', 'authors', 'genres', 'cover image', 'series type', 'series status', 'publish date', 'summary', 'seriesID'])
    currVal = 86153  #last scraped id file  
    #scraped 18039k
    
    while currVal < 1000000:
        start = currVal
        try: 
            for i in range(start,1000000):
                print(i)
                res = scrape_mal(anime_url + str(i))
                if res != []:
                    res.append(str(i))
                    csv_writer.writerow(res)
                    
                time.sleep(3)
                currVal += 1
                
        except: 
            print("curr value is: " + str(currVal))
            currVal += 1
            

# print(scrape_mal(anime_url))