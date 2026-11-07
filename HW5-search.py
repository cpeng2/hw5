"""
HW6 Starter: Linear and Binary Search on video game data.

Purpose: let the user explore a CSV of video games by
  1. console + release year      (LINEAR search)   <- you write this
  2. game title / title prefix   (BINARY search)   <- you write this
  3. best reviewed games by console and genre (provided: filter + selection sort)
  4. top selling games by year                (provided: filter + selection sort)
  5. list of all genres                       (provided)
  6. quit

Provided for you: loading the data, the menu, input checking, table display,
selection sort, the genre/ranking features, and a helper
(look_forward_backward). Your job is the three functions marked TODO in the
"YOUR CODE" section.

Each game is stored as a list ("a row") with these positions:
    0 title (str)       1 max players (int)   2 genre (str)
    3 review score (int) 4 sales (float)       5 used price (float)
    6 console (str)     7 rating (str)         8 year (int)
    9 play length in hours (float, -1 if unknown)
"""

import csv

# Named column positions so you can write row[YEAR] instead of row[8].
TITLE, MAX_PLAYERS, GENRE, REVIEW, SALES, PRICE = 0, 1, 2, 3, 4, 5
CONSOLE, RATING, YEAR, PLAYTIME = 6, 7, 8, 9

DATA_FILE = "./video_games.csv"
MIN_YEAR, MAX_YEAR = 2004, 2008


# ---------------------------------------------------------------------------
# PROVIDED CODE (you do not need to change anything in this section)
# ---------------------------------------------------------------------------

def load_data(filename):
    """Read the CSV and return a list of rows with numbers converted to
    int/float. The file is already sorted by title (case-insensitive)."""
    games = []
    with open(filename, encoding="utf-8") as infile:
        reader = csv.reader(infile)
        next(reader)  # skip the header line
        for row in reader:
            games.append([
                row[0],            # title
                int(row[1]),       # max players
                row[2],            # genre
                int(row[3]),       # review score
                float(row[4]),     # sales (millions)
                float(row[5]),     # used price
                row[6],            # console
                row[7],            # rating
                int(row[8]),       # year
                float(row[9]),     # play length
            ])
    return games


def look_forward_backward(data, start_index, prefix, direction):
    """Starting next to start_index, walk through data in the given direction
    (1 = forward, -1 = backward) and collect rows whose title starts with
    prefix (case-insensitive). Stops at the first title that does not match.
    The row AT start_index is NOT included. Backward matches are returned in
    their original file order."""
    matches = []
    index = start_index + direction
    while 0 <= index < len(data):
        if not data[index][TITLE].lower().startswith(prefix.lower()):
            break
        matches.append(data[index])
        index += direction
    if direction == -1:
        matches.reverse()
    return matches


def display_results(results):
    """Print a list of game rows as a table that fits in 80 columns."""
    print()
    print(f"{'TITLE':30} {'REVIEW':>6} {'SALES':>5} {'PRICE':>5} "
          f"{'CONSOLE':>7} {'YEAR':>4} {'PLAYTIME':>8}")
    print(f"{'-'*30} {'-'*6} {'-'*5} {'-'*5} {'-'*7} {'-'*4} {'-'*8}")
    for game in results:
        print(f"{game[TITLE][:30]:30} {game[REVIEW]:>6} {game[SALES]:>5} "
              f"{game[PRICE]:>5} {game[CONSOLE][:7]:>7} {game[YEAR]:>4} "
              f"{round(game[PLAYTIME], 2):>8}")
    if len(results) == 0:
        print("Sorry, no matches were found.")
    else:
        print(f"{len(results)} matches found")


def get_valid_year():
    """Keep asking until the user types an integer from MIN_YEAR to MAX_YEAR."""
    while True:
        text = input("Enter year: ")
        if text.isdigit() and MIN_YEAR <= int(text) <= MAX_YEAR:
            return int(text)
        print(f"Please enter a year between {MIN_YEAR}-{MAX_YEAR}.")


def print_menu():
    print("1. Search by console and release year")
    print("2. Search by game title")
    print("3. Rank best reviewed games by console and genre")
    print("4. Find top selling games by year")
    print("5. Help: list possible Genres")
    print("6. Quit")


MAX_RANKED_RESULTS = 25


def selection_sort(items, column, descending=True):
    """Sort a list of rows IN PLACE with selection sort, by row[column].
    descending=True puts the largest value first. Returns the list."""
    for start in range(len(items)):
        best = start
        for i in range(start + 1, len(items)):
            if descending:
                if items[i][column] > items[best][column]:
                    best = i
            else:
                if items[i][column] < items[best][column]:
                    best = i
        items[start], items[best] = items[best], items[start]
    return items


def get_genres(data):
    """Return an alphabetical list of the unique genres in the data."""
    genres = []
    for game in data:
        for genre in game[GENRE].split("/"):
            genre = genre.strip()
            if genre != "" and genre not in genres:
                genres.append(genre)
    # selection_sort wants rows, so wrap each genre in a one-item row
    wrapped = [[genre] for genre in genres]
    selection_sort(wrapped, 0, descending=False)
    return [row[0] for row in wrapped]


def rank_by_review(data, console, genre):
    """Option 3: games matching console and genre (either may be 'Any'; genre
    matches partially), best review score first, at most 25 results."""
    matches = []
    for game in data:
        console_ok = console.lower() == "any" or game[CONSOLE].lower() == console.lower()
        genre_ok = genre.lower() == "any" or genre.lower() in game[GENRE].lower()
        if console_ok and genre_ok:
            matches.append(game)
    selection_sort(matches, REVIEW)
    return matches[:MAX_RANKED_RESULTS]


def rank_by_sales(data, year):
    """Option 4: games released in year, best selling first, at most 25."""
    matches = []
    for game in data:
        if game[YEAR] == year:
            matches.append(game)
    selection_sort(matches, SALES)
    return matches[:MAX_RANKED_RESULTS]


def show_genres(data):
    print("List of game genres in the data set:")
    print("-" * 36)
    for genre in get_genres(data):
        print(genre)


# ---------------------------------------------------------------------------
# YOUR CODE
# ---------------------------------------------------------------------------

def linear_search_console_year(data, console, year):
    """Return a list of ALL rows whose console and year both match.

    - Compare console in lowercase so the search is case-insensitive.
    - Return the original rows (keep their original capitalization).
    - Return an empty list if nothing matches.
    """
    # TODO: loop over every row, collect the ones that match, return them.
    matches = []
    for game in data:
        if game[YEAR] == year and game[CONSOLE].lower() == console.lower():
            matches.append(game)
    return matches


def binary_search_title(data, prefix):
    """Return the index of ANY row whose title starts with prefix, or -1.

    data is sorted by title, so use binary search (do NOT loop over everything).
    - Compare in lowercase.
    - Use .startswith(prefix) to test for a match (not ==).
    - If the middle title does not start with prefix, decide which half
      to keep by comparing prefix to the middle title.
    """
    # TODO: set low and high, then repeat: look at the middle row.
    #   - title starts with prefix -> return mid
    #   - prefix comes BEFORE the middle title -> search the lower half
    #   - otherwise -> search the upper half
    # If low passes high, nothing matched.
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        current = data[mid][TITLE]
        if current.lower().startswith(prefix.lower()):
            return mid
        elif prefix.lower() < current.lower():
            high = mid - 1
        else:
            low = mid + 1  
    return -1


def search_by_title(data, prefix):
    """Return ALL rows whose title starts with prefix.

    Binary search only gives you ONE match. Games with the same title (or the
    same start, like 'LEGO') sit next to each other, so use the match as a
    starting point and call look_forward_backward in both directions.
    Return the matches in file order (backward matches, the seed row, then
    forward matches). Return [] if binary search finds nothing.
    """
    # TODO: 1) seed_index = binary_search_title(data, prefix)
    #       2) if it is -1, return []
    #       3) call look_forward_backward twice (-1 and 1)
    #       4) combine: backward matches + [data[seed_index]] + forward matches
    return []



# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    games = load_data(DATA_FILE)
    print("This program helps the user explore a data set of")
    print("over a thousand video games released between")
    print("2004 and 2008.")

    while True:
        print_menu()
        choice = input("Choice: ")
        if choice == "1":
            year = get_valid_year()
            console = input("Enter console: ")
            display_results(linear_search_console_year(games, console, year))
        elif choice == "2":
            prefix = input("Enter game title (or start of title): ")
            display_results(search_by_title(games, prefix))
        elif choice == "3":
            console = input("Enter console (or 'Any'): ")
            genre = input("Enter genre (or 'Any'): ")
            display_results(rank_by_review(games, console, genre))
        elif choice == "4":
            year = get_valid_year()
            display_results(rank_by_sales(games, year))
        elif choice == "5":
            show_genres(games)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
