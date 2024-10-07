import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  # Import WebDriver Manager
import pyodbc
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

def scrape_imdb_top_250():
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250&sort=runtime%2Casc'
    
    # Set up the Chrome WebDriver using WebDriver Manager
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={headers['User-Agent']}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(3)
    
    # Click the button to trigger the detailed view
    try:
        # Locate the button by ID and click it
        button = driver.find_element(By.ID, 'list-view-option-detailed')
        button.click()
        time.sleep(2)  # Wait for the page to load the detailed view
    except Exception as e:
        print(f"Error clicking the button: {e}")

    # Find all movies listed in the Top 250 table
    movies = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item__c')

    movie_list = []

    for movie in movies:
        # Extract title
        title_column = movie.find_element(By.CLASS_NAME, 'ipc-title__text')
        full_title = title_column.text.strip()

        # Check if the title contains a period before splitting
        if '.' in full_title:
            title = full_title.split('.', 1)[1].strip()
        else:
            title = full_title  # If no period, use the entire title


        # Split the title by the first occurrence of '.' and get the part after it
        title = full_title.split('.', 1)[1].strip()
        
        # Extract year
        year_text = movie.find_element(By.XPATH, './/span[contains(@class, "sc-ab348ad5-8")]').text.strip() if movie.find_elements(By.XPATH, './/span[contains(@class, "sc-ab348ad5-8")]') else None
        year = year_text if year_text else None

        # Extract IMDb rating
        imdb_rating = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--rating').text.strip()
        imdb_rating = float(imdb_rating) if imdb_rating else None

        # Extract rating count
        rating_count = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--voteCount').text.strip() if movie.find_elements(By.CLASS_NAME, 'ipc-rating-star--voteCount') else 'N/A'

        # Extract description
        description = movie.find_element(By.CLASS_NAME, 'ipc-html-content-inner-div').text.strip() if movie.find_elements(By.CLASS_NAME, 'ipc-html-content-inner-div') else 'N/A'

        # Extract director
        director = "N/A"
        try:
            director = movie.find_element(By.XPATH, './/span[contains(@class, "sc-59c7dc1-5")]/a[contains(@class, "ipc-link ipc-link--base dli-creator-item")]').text.strip()
        except:
            pass
        
        # Extract starring 
        stars = [star.text.strip() for star in movie.find_elements(By.XPATH, './/span/a[@class="ipc-link ipc-link--base dli-cast-item"]')]

        # Extract image URL
        image_element = movie.find_element(By.XPATH, './/div/img[@class="ipc-image"]')
        image_url = image_element.get_attribute('src')  # Extract the 'src' attribute from the image tag

        # Extract episodes
        episodes = movie.find_element(By.XPATH, './/span[contains(text(),"eps")]').text.strip() if movie.find_elements(By.XPATH, './/span[contains(text(),"eps")]') else 'N/A'

        # TV GENRE 'TV Series'
        genre = movie.find_element(By.XPATH, './/span[contains(@class, "sc-ab348ad5-3") and contains(text(), "TV")]').text.strip() if movie.find_elements(By.XPATH, './/span[contains(@class, "sc-ab348ad5-3") and contains(text(), "TV")]') else 'N/A'

        # Extract TV rating (e.g., TV-MA)
        tv_rating = movie.find_element(By.XPATH, './/span[contains(@class, "sc-ab348ad5-8") and contains(text(),"TV")]').text.strip() if movie.find_elements(By.XPATH, './/span[contains(@class, "sc-ab348ad5-8") and contains(text(),"TV")]') else 'N/A'

            

        # Append the scraped data to the movie list
        movie_list.append({
            'Title': title,
            'Year': year,
            'IMDb Rating': imdb_rating,
            'Rating Count': rating_count,
            'Description': description,
            #'Director': director,
            'Stars': ", ".join(stars),
            #'Episodes': episodes,
        
          
            'Image URL': image_url
        })


    driver.quit()

    return movie_list


# # Function to insert data into SQL Server
def insert_into_database(movies):
    # SQL Server connection setup with Windows Authentication
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LENOVO-PC\SQLEXPRESS;'  # my sql server name
        'DATABASE=project2;'  # my sql database name
        'Trusted_Connection=yes;'
    )
    
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute(''' 
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='IMDB_Top_250_movies_runtime' AND xtype='U')
    BEGIN
        CREATE TABLE IMDB_Top_250_movies_runtime (
            id INT IDENTITY(1,1) PRIMARY KEY,  -- Auto-incrementing primary key
            Title NVARCHAR(255) NOT NULL,      -- Title of the TV show
            Year NVARCHAR(10),                 -- Year of release (can store a range like "2008-2013")
            IMDB_Rating FLOAT,                 -- IMDb rating (stored as a float)
            Rating_Count NVARCHAR(20),         -- Rating count (e.g., "2.9M")
            Description VARCHAR(MAX),          -- Description of the TV show
            
            Stars VARCHAR(255),                -- Comma-separated list of star actors
            
          
            ImageURL NVARCHAR(MAX)          -- Get the image url
        )
    END
    ''')

    # Insert data into the table
    for movie in movies:
        cursor.execute('''
            INSERT INTO IMDB_Top_250_movies_runtime 
            (Title, Year, IMDB_Rating, Rating_Count, Description, Stars, ImageURL)
            VALUES (?, ?, ?, ?, ?, ?, ? )
        ''', 
        movie['Title'], 
        movie['Year'], 
        movie['IMDb Rating'], 
        movie['Rating Count'], 
        movie['Description'], 
        movie['Stars'],   
       
        movie['Image URL'],
    )
    connection.commit()
    cursor.close()
    connection.close()

# Main function
if __name__ == '__main__':
    # Scrape the data
    movies = scrape_imdb_top_250()
    
    if movies:
        print(f"Scraped Top {len(movies)} movies successfully!")
        
        # Insert the scraped data into SQL Server
        insert_into_database(movies)
        print('Data written in SQL Tables')
    else:
        print("No data scraped.")
