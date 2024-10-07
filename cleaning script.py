import pandas as pd

def clean_year(year):
    """Extract the year and convert it to an integer."""
    if pd.isna(year):
        return None  # Handle NaN values
    try:
        return int(str(year).split('–')[0].strip())
    except ValueError:
        return None  # Return None if conversion fails

def clean_rating(rating):
    """Convert rating to float."""
    if pd.isna(rating):
        return None  # Handle NaN values
    try:
        return float(rating)
    except ValueError:
        return None  # Return None if conversion fails

def clean_votes(votes):
    """Remove commas from votes and convert to integer."""
    if pd.isna(votes):
        return None  # Handle NaN values
    try:
        return int(votes.replace(',', '').strip())
    except ValueError:
        return None  # Return None if conversion fails

# Read the CSV file
csv_file = r'C:\Users\Maroof\Desktop\IMDB Data engineering project\IMBD_movies.csv'
df = pd.read_csv(csv_file)

# Clean the columns
df['year'] = df['year'].apply(clean_year)
df['rating'] = df['rating'].apply(clean_rating)
df['votes'] = df['votes'].apply(clean_votes)

# Save the cleaned DataFrame to a new CSV file
cleaned_csv_file = r'C:\Users\Maroof\Desktop\IMDB Data engineering project\IMBD_cleaned.csv'
df.to_csv(cleaned_csv_file, index=False)

print("Data has been cleaned and saved to", cleaned_csv_file)
