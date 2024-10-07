import requests
from bs4 import BeautifulSoup
import pandas as pd



movie_links=[]
names=[]
ratings=[]
years=[]
ranks=[]

try:
    # URL of the IMDb Top 250 Movies page

    url = 'https://www.imdb.com/chart/top/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status() 
    

    soup = BeautifulSoup(response.text,'html.parser')
    movies=soup.find('tbody', class_="lister-list").find_all('tr')

    for movie in movies:
        name=movie.find('td', class_="titleColumn").a.text
        names.append(name)
        rank =movie.find('td', class_="titleColumn").get_text(strip=True).split('.')[0]
        ranks.append(rank)
        year =movie.find('td', class_="titleColumn").span.text.strip('()')
        years.append(year)
        rating = movie.find('td', class_="ratingColumn imdbRating").strong.text
        ratings.append(rating)
        
        
        link_element = movie.find('a', href=True)
        
        if link_element:
            movie_link = 'https://www.imdb.com' + link_element['href']
            movie_links.append(movie_link)
        else:
            movie_links.append('N/A')

except Exception as e:
    print(e)


    
   
        
       

    # Create a DataFrame to store the scraped data
    movies_data = pd.DataFrame({
        'Rank':ranks,
        'Title': names,
        'year':years,
        'Rating': ratings,
        'IMDb Link': movie_links
    })
    # Save the data to a CSV file
    movies_data.to_csv('imdb_top_250_movies.csv', index=False)
    # Display the DataFrame
    print(movies_data.head())
