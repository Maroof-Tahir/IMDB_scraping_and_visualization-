import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv(r'C:\Users\Maroof\Desktop\IMDB Data engineering project\IMBD_cleaned.csv')
data.columns = data.columns.str.strip()

if 'year' in data.columns and data['year'].dtype == 'object':
    data['start_year'] = data['year'].str.extract(r'(\d{4})').astype(float)
    data['end_year'] = data['year'].str.extract(r'[\–-](\d{4})').astype(float) 
    data.drop(columns=['year'], inplace=True)

print("Columns after year extraction:", data.columns)


data['certificate'] = data['certificate'].fillna('Unknown')


data['duration'] = data['duration'].astype(str).str.replace(' min', '', regex=False).astype(float)


data['genre'] = data['genre'].fillna('Unknown')


data['votes'] = pd.to_numeric(data['votes'].astype(str).str.replace(',', '', regex=False), errors='coerce').fillna(0).astype(int)


if data['stars'].apply(lambda x: isinstance(x, list)).any():
    data['stars'] = data['stars'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
            
data['stars'] = data['stars'].astype(str).str.strip("[]").str.replace("'", "").str.split(", ")


data_without_stars = data.drop(columns=['stars']).drop_duplicates()


data = pd.concat([data_without_stars, data['stars']], axis=1)


data.dropna(subset=['rating', 'duration'], inplace=True)


if 'start_year' in data.columns:
    data.drop_duplicates(subset=['title', 'start_year'], inplace=True)
else:
    print("start_year column not found, skipping duplicate removal based on it.")


imdb_yellow = '#F5C518'

def menu():
    print("\nIMDB Data Engineering Project Menu:")
    print("1. Plot for Distribution of ratings")
    print("2. Plot for Votes vs Ratings")
    print("3. Plot for Count of Certificates")
    print("4. Plot for Most Common Genres")
    print("5. Plot for Average ratings by certificates")
    print("6. Plot for Highest Rated Movies")
    print('7. Plot for Average Ratings by Genre')
    print('8. Plot for Average Ratings by Certificate')
    print('9. Detail of the data')
    print('10. Get data info')
    print('11. Data description')
    print('12. Exit')
    user_input=int(input("Choose the appropriate option: "))


    if user_input==1:
        plt.figure(figsize=(10, 6))
        data['rating'].hist(bins=20, color=imdb_yellow)
        plt.title('Distribution of Ratings')
        plt.xlabel('Rating')
        plt.ylabel('Frequency')
        plt.show()
    elif user_input==2:
        plt.figure(figsize=(10, 6))
        plt.scatter(data['votes'], data['rating'], color=imdb_yellow)
        plt.title('Votes vs. Rating')
        plt.xlabel('Votes')
        plt.ylabel('Rating')
        plt.show()
    elif user_input==3:
        plt.figure(figsize=(10, 6))
        sns.countplot(y=data['certificate'], order=data['certificate'].value_counts().index, color=imdb_yellow)
        plt.title('Count of Certificates')
        plt.xlabel('Count')
        plt.ylabel('Certificate')
        plt.show()
    elif user_input==4:
        plt.figure(figsize=(10, 6))
        data['genre'].explode().value_counts().head(10).plot(kind='barh', color=imdb_yellow)
        plt.title('Top 10 Most Common Genres')
        plt.xlabel('Count')
        plt.ylabel('Genre')
        plt.show()
    elif user_input==5:
        # avg ratings by certificates
        avg_rating_by_cert = data.groupby('certificate')['rating'].mean().sort_values()
        print("Average Rating by Certificate:")
        print(avg_rating_by_cert)
    elif input==6:
        top_rated_movies = data.sort_values(by='rating', ascending=False)
        top_10_rated_movies = top_rated_movies.head(10)
        plt.figure(figsize=(10, 6))
        plt.barh(top_10_rated_movies['title'], top_10_rated_movies['rating'], color='#F5C518')
        plt.gca().invert_yaxis()  # Invert y-axis to have the highest-rated movie at the top
        plt.title('Top 10 Highest Rated Movies')
        plt.xlabel('Rating')
        plt.ylabel('Movie Title')
        plt.show()
    elif user_input==7:
        avg_rating_by_genre = data.explode('genre').groupby('genre')['rating'].mean().sort_values()
        print("\nAverage Rating by Genre:")
        print(avg_rating_by_genre)
    elif user_input ==8:
        plt.figure(figsize=(10, 6))
        avg_rating_by_cert = data.groupby('certificate')['rating'].mean().sort_values()
        avg_rating_by_cert.plot(kind='barh', color='#F5C518')
        plt.title('Average Rating by Certificate')
        plt.xlabel('Average Rating')
        plt.ylabel('Certificate')
        plt.show()
    elif user_input==9:
        # Detail of the data Number of entries , no of columns
        print('The Length of data entries and number of columns: ')
        print(data.shape)
    elif user_input ==10:
        print(data.info())
    elif user_input ==11:
        # total na data 
        print(data.isna().sum())
        # description 
        print(data.describe())
    elif user_input==12:
        exit()
# distinguishing unique stats
columns_to_exclude = ['stars', 'genre']

unique_counts = data.drop(columns=columns_to_exclude).nunique()

print("\nUnique values in columns without lists:")
print(unique_counts)

unique_genres = data['genre'].explode().nunique()
print(f"\nUnique genres: {unique_genres}")

unique_stars = data['stars'].explode().nunique()
print(f"\nUnique stars: {unique_stars}")

if __name__ == '__main__':
    while(1):
        menu()