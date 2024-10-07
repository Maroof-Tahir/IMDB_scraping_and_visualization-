import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Function to fetch movie data from a single IMDb page
def get_movie_data(imdb_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    # Send an HTTP request to fetch the HTML content
    response = requests.get(imdb_url, headers=headers)
    
    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    movies = []
    
    # Select all movie containers
    movie_containers = soup.select('div.lister-item.mode-advanced')
    
    # Loop through each movie container and extract information
    for movie in movie_containers:
        title = movie.h3.a.text
        year = movie.h3.find('span', class_='lister-item-year').text.strip('()')
        certificate = movie.p.find('span', class_='certificate').text if movie.p.find('span', class_='certificate') else 'Not Rated'
        duration = movie.p.find('span', class_='runtime').text if movie.p.find('span', class_='runtime') else 'Unknown'
        genre = movie.p.find('span', class_='genre').text.strip() if movie.p.find('span', class_='genre') else 'Unknown'
        description = movie.find_all('p', class_='text-muted')[1].text.strip()
        stars = movie.select('p > a[href*="/name/"]')
        stars = [star.text for star in stars[:4]]  # Top 4 stars
        votes = movie.find('span', attrs={'name': 'nv'}).text if movie.find('span', attrs={'name': 'nv'}) else '0'

        # Append movie data as a dictionary
        movies.append({
            'Title': title,
            'Year': year,
            'Certificate': certificate,
            'Duration': duration,
            'Genre': genre,
            'Description': description,
            'Stars': stars,
            'Votes': votes
        })
    
    return movies

# Function to get total number of pages
def get_total_pages(imdb_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(imdb_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the total number of pages (based on pagination)
    pagination = soup.select('div.desc span.lister-current-last')
    if pagination:
        total_movies = int(pagination[0].text.replace(',', ''))
        total_pages = total_movies // 50 + 1  # Each page typically contains 50 movies
        return total_pages
    else:
        return 1  # If pagination is not found, only 1 page exists

# Main function to scrape all pages
def scrape_all_imdb_movies():
    base_url = "https://www.imdb.com/search/title/?title_type=feature&sort=num_votes,desc&start={}"
    all_movies = []

    # Get the total number of pages
    total_pages = get_total_pages(base_url.format(1))
    print(f"Total pages to scrape: {total_pages}")
    
    # Loop through each page
    for page in range(1, total_pages + 1):
        print(f"Scraping page {page} of {total_pages}...")
        
        # Generate the page URL dynamically
        imdb_url = base_url.format((page - 1) * 50 + 1)
        
        # Get movie data for the current page
        movie_data = get_movie_data(imdb_url)
        
        # Append to the overall list
        all_movies.extend(movie_data)
        
        # Pause between requests to avoid being blocked
        time.sleep(1)

    # Convert to DataFrame for easy handling
    df = pd.DataFrame(all_movies)

    # Save data to CSV file
    df.to_csv('IMDB.csv', index=False)

    print("All movie data saved to imdb.csv")

# Run the scraper
if __name__ == "__main__":
    scrape_all_imdb_movies()
