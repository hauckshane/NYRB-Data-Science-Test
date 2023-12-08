
import requests
from bs4 import BeautifulSoup
import csv
import time


def get_data(type):
    """
    Scrapes Match Log data from FBREF for all MLS games 2018-2023.

    Args:
        type (str): The type of data to scrape.

    Returns:
        list: A list of lists containing the scraped data.
    """
    clubs = ['FC-Cincinnati', 'Orlando-City', 'Columbus-Crew',
             'Philadelphia-Union', 'New-England-Revolution',
             'Atlanta-United', 'Nashville-SC', 'New-York-Red-Bulls',
             'Charlotte-FC', 'DC-United', 'New-York-City-FC',
             'CF-Montreal', 'Toronto-FC', 'Chicago-Fire', 'Inter-Miami',
             'FC-Dallas', 'Houston-Dynamo', 'Minnesota-United',
             'Sporting-Kansas-City', 'Colorado-Rapids', 'Real-Salt-Lake',
             'LA-Galaxy', 'Portland-Timbers', 'San-Jose-Earthquakes',
             'Seattle-Sounders', 'Vancouver-Whitecaps', 'Austin-FC',
             'Los-Angeles-FC', 'St-Louis-City']

    teamcode = [
        'e9ea41b2', '46ef01d0', '529ba333', '46024eeb', '3c079def', '1ebc1a5b',
        '35f1b818', '69a0fb10', 'eb57545a', '44117292', '64e81410', 'fc22273c',
        '130f43fa', 'f9940243', 'cb8b86a2', '15cf8f40', '0d885416', '99ea75a6',
        '4acb0537', '415b4465', 'f7d86a43', 'd8b46897', 'd076914e', 'ca460650',
        '6218ebd4', 'ab41cb90', 'b918956d', '81d817a3', 'bd97ac1f']

    years = [2023, 2022, 2021, 2020, 2019, 2018]

    data = []

    gameid = 0

    for year in years:
        print(year)
        if year == 2022:
            teamcode.remove(teamcode[clubs.index('St-Louis-City')])
            clubs.remove('St-Louis-City')
        if year == 2021:
            teamcode.remove(teamcode[clubs.index('Charlotte-FC')])
            clubs.remove('Charlotte-FC')
        if year == 2020:
            teamcode.remove(teamcode[clubs.index('Austin-FC')])
            clubs.remove('Austin-FC')
        if year == 2019:
            teamcode.remove(teamcode[clubs.index('Inter-Miami')])
            clubs.remove('Inter-Miami')
            teamcode.remove(teamcode[clubs.index('Nashville-SC')])
            clubs.remove('Nashville-SC')
        if year == 2018:
            teamcode.remove(teamcode[clubs.index('Los-Angeles-FC')])
            clubs.remove('Los-Angeles-FC')
            teamcode.remove(teamcode[clubs.index('FC-Cincinnati')])
            clubs.remove('FC-Cincinnati')
        # Iterate over each club
        for club in clubs:
            # Construct the URL for the club and year
            club_index = clubs.index(club)
            url = f"https://fbref.com/en/squads/{teamcode[club_index]}/{year}/matchlogs/c22/{type}/{club}-Match-Logs-Major-League-Soccer"

            # Send a GET request to the website
            response = requests.get(url)

            # Create a BeautifulSoup object to parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the table with the specified ID
            table = soup.find(id="div_matchlogs_for")

            # Check if the table exists
            if table is not None:
                # Extract the data from the table
                for row in table.find_all("tr"):
                    row_data = [gameid] + [year] + [club] + [cell.get_text(strip=True)
                                                  for cell in row.find_all("td")]
                    print(row_data)
                    if row_data and 'NA' not in row_data:
                        data.append(row_data)
                        gameid += 1
            time.sleep(3)
    return data


def get_data_bundesliga(type):
    """
    Scrapes Match Log data from FBREF for all Bundesliga games 2018-2023.

    Args:
        type (str): The type of data to scrape.

    Returns:
        list: A list of lists containing the scraped data.
    """
    clubs = ['Bayern-Munich', 'Dortmund', 'RB-Leipzig',
             'Bayer-Leverkusen', 'Monchengladbach',
             'Wolfsburg', 'Eintracht-Frankfurt', 'Union-Berlin',
             'Stuttgart', 'Freiburg', 'Hoffenheim',
             'Augsburg', 'Hertha-BSC', 
             'Mainz-05', 'Koln', 'Werder-Bremen', 'Schalke-04', 'Bochum',
             'Arminia', 'Greuther-Furth', 'Dusseldorf', 'Paderborn-07', 'Hannover-96',
             'Nurnberg', 'Hamburger-SV']

    teamcode = ['054efa67','add600ae','acbb6a5b','c7a9f859','32f3ee20','4eaa11d7', 'f0ac8ee6',
                '7a41008f','598bc722','a486e511','033ea6b8','0cdc4311','2818f8bc','a224b06a',
                'bc357bf7','62add3bf','c539e393','b42c6323',
                '247c4b67','12192a4c','b1278397','d9f93f02', '60b5e41f', '6f2c108c','26790c6a']

    years = [2023, 2022, 2021, 2020, 2019, 2018]

    data = []

    for year in years:
        print(year)
    
        # Iterate over each club
        for club in clubs:
            # Construct the URL for the club and year
            club_index = clubs.index(club)
            url = f"https://fbref.com/en/squads/{teamcode[club_index]}/{year-1}-{year}/matchlogs/all_comps/{type}/{club}-Match-Logs-All-Competitions"

            # Send a GET request to the website
            response = requests.get(url)

            # Create a BeautifulSoup object to parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the table with the specified ID
            table = soup.find(id="div_matchlogs_for")

            # Check if the table exists
            if table is not None:
                # Extract the data from the table
                for row in table.find_all("tr"):
                    row_data = [year] + [club] + [cell.get_text(strip=True)
                                                  for cell in row.find_all("td")]
                    print(row_data)
                    if row_data and 'NA' not in row_data:
                        data.append(row_data)
            time.sleep(3)
    return data


def write_csv(value, data, headers):
    """
    Writes the scraped data to a CSV file.

    Args:
        value (str): The name of the CSV file to write to.
        data (list): The data to write to the CSV file.
        headers (list): The column headers for the CSV file.

    Returns:
        None
    """
    with open(f"{value}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # Write the column headers
        writer.writerow(headers)
        # Write the data rows
        writer.writerows(data)
    


def get_shooting():
    """
    Retrieves shooting data and saves it to a CSV file.

    Returns:
        None
    """

    # Define the column headers
    headers = ["Year", "Club", "Time", "Round", "Day", "Venue", "Result", "GF",
               "GA", "Opponent", "Gls", "Sh", "SoT", "SoT_pct", "G/Sh", "G/SoT",
               "Dist", "FK", "PK", "PKatt", "xG", "npxG", "npxGperShot", "G-xG",
               "npG-xG", "Match_Report"]

    data = get_data_bundesliga('shooting')

    write_csv('BD_shooting', data, headers)


def get_passing():
    """
    Retrieves passing data and saves it to a CSV file.

    Returns:
        None
    """

    # Define the column headers
    headers = ["Year", "Club", "Time", "Round", "Day", "Venue", "Result", "GF",
               "GA", "Opponent", "Total_Cmp", "Total_Att", "Cmp_pct", "TotDist",
               "PrgDist", "Short_Cmp", "Short_Att", "Short_Cmp_pct", "Med_Cmp", 
               "Med_Att", "Med_Cmp_pct","Long_Cmp", "Long_Att", "Long_Cmp_pct",
               "Ast", "xAG", "xA", "KP", "1/3", "PPA", "CrsPA", "PrgP", "Match_Report"]

    data = get_data_bundesliga('passing')

    write_csv('BD_passing', data, headers)


def get_passtypes():
    """
    Retrieves pass type data and saves it to a CSV file.

    Returns:
        None
    """

    # Define the column headers
    headers = ["Year", "Club", "Time", "Round", "Day", "Venue", "Result", "GF",
               "GA", "Opponent", "Att", "Live", "Dead", "FK", "TB", "Sw", "Crs",
               "TI", "CK", "CKIn", "CKOut", "Str", "Cmp", "Off", "Blocks", "Match_Report"]

    data = get_data_bundesliga('passing_types')

    write_csv('BD_passing_types', data, headers)


def get_gca():
    """
    Retrieves goal and shot creation data and saves it to a CSV file.

    Returns:
        None
    """

    # Define the column headers
    headers = ["Year", "Club", "Time", "Round", "Day", "Venue", "Result", "GF",
               "GA", "Opponent", "SCA", "SCA_PassLive", "SCA_passDead", "SCA_TO", 
               "SCA_Sh", "SCA_Fld", "SCA_Def", "GCA", "GCA_PassLive", "GCA_PassDead",
               "GCA_TO", "GCA_Sh", "GCA_Fld", "GCA_Def", "Match_Report"]

    data = get_data_bundesliga('gca')

    write_csv('BD_gca', data, headers)


def get_defense():
    """
    Retrieves defensive action data and saves it to a CSV file.

    Returns:
        None
    """

    # Define the column headers
    headers = ["Year", "Club", "Time", "Round", "Day", "Venue", "Result", "GF",
               "GA", "Opponent", "Tkl", "TklW", "Tkl_Def_3rd", "Tkl_Mid_3rd", "Tkl_Att_3rd",
               "Tkl_Succ", "Tkl_Att", "Tkl_pct", "Tkl_Lost", "Blocks", "Blocks_Shot", "Blocks_Pass",
               "Int", "Tkl+Int", "Clr", "Err", "Match_Report"]

    data = get_data_bundesliga('defense')

    write_csv('BD_defense', data, headers)


def get_possession():
    """
    Retrieves possession data and saves it to a CSV file.

    Returns:
        None
    """

    # Define the column headers
    headers = ["Year", "Club", "Time", "Round", "Day", "Venue", "Result", "GF",
               "GA", "Opponent", "Poss", "Touches", "Touches_DefPen", "Touches_Def3rd", "Touches_Mid3rd",
               "Touches_Att3rd", "Touches_AttPen", "Touches_Live", "Drib_Att", "Drib_Succ", "Drib_Succ_pct",
               "Drib_Tkld", "Drib_Tkld_pct", "Carries", "Carries_TotDist", "Carries_PrgDist", "Carries_Prg",
               "Carries_1/3", "Carries_CPA", "Carries_Mis", "Carries_Dis", "Pass_Receptions", "Pass_Receptions_Prg",
               "Match_Report"]

    data = get_data_bundesliga('possession')

    write_csv('BD_possession', data, headers)


def get_misc():
    """
    Retrieves miscellaneous data and saves it to a CSV file.

    Returns:
        None
    """

    # Define the column headers
    headers = ["Year", "Club", "Time", "Round", "Day", "Venue", "Result", "GF",
               "GA", "Opponent", "CrdY", "CrdR", "2CrdY", "Fls", "Fld", "Off",
               "Crs", "Int", "TklW", "PKwon", "PKcon", "OG", "Recov", "Aerial_Won",
               "Aerial_Lost", "Aerial_Win_pct", "Match_Report"]

    data = get_data_bundesliga('misc')

    write_csv('BD_misc', data, headers)


get_shooting()
get_passing()
get_passtypes()
get_gca()
get_defense()
get_possession()
get_misc()
