import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

# Predefined file paths
file_paths = {
    1: {"path": r"C:\Users\Softtech User\Desktop\IMDB\Project 2\LowestRated\byAlphabetic.py", "table": "IMDB_Top_lowRate_byalphabetic"},
    2: {"path": r"C:\Users\Softtech User\Desktop\IMDB\Project 2\LowestRated\byNumRating.py", "table": "IMDB_Top_lowRate_bynumRate"},
    3: {"path": r"C:\Users\Softtech User\Desktop\IMDB\Project 2\LowestRated\byPopularity.py", "table": "IMDB_Top_lowRate_bypopularity"},
    4: {"path": r"C:\Users\Softtech User\Desktop\IMDB\Project 2\LowestRated\byReleaseDate.py", "table": "IMDB_Top_lowRate_byrealeaseDate"},
    5: {"path": r"C:\Users\Softtech User\Desktop\IMDB\Project 2\LowestRated\byRuntime.py", "table": "IMDB_Top_lowRate_byRuntime"},
    6: {"path": r"C:\Users\Softtech User\Desktop\IMDB\Project 2\LowestRated\byUserRating.py", "table": "IMDB_Top_lowRate_byRating"},
    7: {"path": r"C:\Users\Softtech User\Desktop\IMDB\Project 2\LowestRated\lowestRated.py", "table": "IMDB_Top_lowRate"}
}

# Function to load data from SQL Server
def load_data_from_sql(table_name):
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-J2KJLA0\SQLEXPRESS;'   
        'DATABASE=FinalProject;'   
        'Trusted_Connection=yes;'
    )
    
    query = f"SELECT Title, IMDB_Rating FROM {table_name}"
    df = pd.read_sql(query, connection)
    connection.close()
    
    return df

# Function to plot a bar chart
def plot_bar_chart(df, file_number, title_suffix):
    # Get the first and last 6 movies
    movies_to_plot = pd.concat([df.head(6), df.tail(6)])
    
    # Create color gradient based on the rating
    norm = plt.Normalize(movies_to_plot['IMDB_Rating'].min(), movies_to_plot['IMDB_Rating'].max())
    cmap = mcolors.LinearSegmentedColormap.from_list("rating_cmap", ['#d9e3f0', '#365a9e'])  # Light to dark blue
    
    # Create bar chart
    plt.figure(figsize=(10, 8))
    bar_colors = cmap(norm(movies_to_plot['IMDB_Rating']))  # Generate colors based on the rating
    bars = plt.barh(movies_to_plot['Title'], movies_to_plot['IMDB_Rating'], color=bar_colors)

    # Add rating values on the bars
    for bar, value in zip(bars, movies_to_plot['IMDB_Rating']):
        plt.text(value, bar.get_y() + bar.get_height()/2, f'{value:.1f}', va='center', color='black')

    plt.xlabel('IMDb Rating')
    plt.ylabel('Movie Title')
    plt.title(f'{title_suffix}: IMDb Ratings of First and Last 6 Movies')
    plt.gca().invert_yaxis()  # Invert y-axis to display the first movie at the top
    plt.show()

# Function to display charts in sequence
def show_charts_in_sequence(selected_files):
    for file_number in selected_files:
        table_name = file_paths[file_number]['table']
        df = load_data_from_sql(table_name)
        title_suffix = f"File {file_number}"
        plot_bar_chart(df, file_number, title_suffix)

# Main function
def main():
    print("Choose a file to view:")
    print("1 - Alphabetic")
    print("2 - Num Rating")
    print("3 - Popularity")
    print("4 - Release Date")
    print("5 - Runtime")
    print("6 - User Rating")
    print("7 - Lowest Rated")
    print("8 - Type 'all' to see all files sequentially")
    print("0 - Exit")

    while True:
        choice = input("Enter your choice: ").lower()
        
        if choice == 'all':
            show_charts_in_sequence(range(1, 8))  # Show all charts in sequence
            break
        elif choice.isdigit() and 1 <= int(choice) <= 7:
            file_number = int(choice)
            show_charts_in_sequence([file_number])
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select again.")

# Run the main function
if __name__ == '__main__':
    main()
