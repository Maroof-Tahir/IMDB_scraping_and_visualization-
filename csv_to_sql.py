import pandas as pd
import pyodbc
import re  # Importing the regex module for cleaning

def clean_year(year):
    # Remove non-digit characters, then convert to int
    if isinstance(year, float) and pd.isna(year):  # Check if year is NaN
        return None
    year_cleaned = re.sub(r'\D', '', str(year))  # Ensure it's treated as a string
    return int(year_cleaned) if year_cleaned else None  # Convert to int if not empty

def clean_votes(votes):
    # Check for NaN values
    if isinstance(votes, float) and pd.isna(votes):
        return None
    # Handle both string and float representations
    votes_cleaned = str(votes).replace(',', '').strip()  # Clean the string
    return int(float(votes_cleaned)) if votes_cleaned else None  # Convert to float first, then to int

def insert_into_database(df):
    # SQL Server connection setup
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LENOVO-PC\SQLEXPRESS;'  # Change to your SQL Server name
        'DATABASE=project2;'  # Change to your database name
        'Trusted_Connection=yes;'
    )
    
    cursor = connection.cursor()

    # Create table if it doesn't exist (Optional)
    cursor.execute(''' 
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='IMDB_movies' AND xtype='U')
    BEGIN
        CREATE TABLE IMDB_movies (
            id INT IDENTITY(1,1) PRIMARY KEY,
            Title NVARCHAR(255) NOT NULL,
            Year INT,
            Certificate NVARCHAR(10),
            Duration NVARCHAR(20),
            Genre NVARCHAR(255),
            Description NVARCHAR(MAX),
            Stars NVARCHAR(255),
            Votes INT
        )
    END
    ''')

    # Insert data into the table
    for index, row in df.iterrows():  # Unpack the tuple correctly
        cursor.execute('''
            INSERT INTO IMDB_movies 
            (Title, Year, Certificate, Duration, Genre, Description, Stars, Votes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', 
        row['title'], 
        clean_year(row['year']),  # Use the cleaned year
        row['certificate'], 
        row['duration'], 
        row['genre'],
        row['description'], 
        row['stars'],   
        clean_votes(row['votes'])  # Use the cleaned votes
        )

    connection.commit()
    cursor.close()
    connection.close()

# Main function
if __name__ == '__main__':
    # Read the CSV file
    csv_file = r'C:\Users\Maroof\Desktop\IMDB Data engineering project\IMBD_cleaned.csv'  # Update the path to your CSV file
    df = pd.read_csv(csv_file)
    print(df.isnull().sum())  # Check for missing values

    # Check for missing values and clean data
    print(df.head())  # Print first few rows to check data
    insert_into_database(df)
    print("Data has been successfully inserted into the database.")
