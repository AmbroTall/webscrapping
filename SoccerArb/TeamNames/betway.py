# ENG Premier League
English_Premier_League = ['Arsenal', 'Aston Villa', 'Bournemouth (AFC Bournemouth)', 'Brentford (Brentford FC)', 'Brighton & Hove Albion (Brighton)', 'Burnley (Burnley FC)', 'Chelsea', 'Everton (Everton FC)',
                          'Crystal Palace', 'Fulham', 'Liverpool (Liverpool FC)', 'Luton Town', 'Manchester City (Man City)', 'Manchester United (Man Utd)', 'Newcastle United',
                          'Nottingham Forest', 'Sheffield United ', 'Tottenham Hotspur (Tottenham)', 'West Ham United', 'Wolverhampton Wanderers (Wolves)']

# ENG Championship
English_Football_League = ['Birmingham City', 'Blackburn Rovers (Blackburn)', 'Bristol City', 'Cardiff City (Cardiff)', 'Coventry City', 'Huddersfield Town (Huddersfield)',
                           'Hull City', 'Ipswich Town', 'Leeds United', 'Leicester City (Leicester)', 'Middlesbrough', 'Millwall', 'Norwich City',
                           'Plymouth Argyle', 'Preston North End', 'Queens Park Rangers QPR (QPR)', 'Rotherham United (Rotherham Utd)', 'Sheffield Wednesday',
                           'Southampton', 'Stoke City', 'Sunderland (Sunderland AFC)' , 'Swansea City ', 'Watford (Watford FC)', 'West Bromwich Albion (West Brom)']

# ENG League One
England_League_One = ['Barnsley', 'Bolton (Bolton Wanderers)', 'Exeter City', 'Blackpool', 'Cambridge United', 'Charlton (Charlton Athletic)', 'Peterborough (Peterborough United)', 'Shrewsbury (Shrewsbury Town)',
                      'Stevenage (Stevenage FC)', 'Portsmouth', 'Carlisle United (Carlisle Utd)', 'Fleetwood Town (Fleetwood)', 'Bristol Rovers', 'Derby County', 'Leyton Orient London',
                      'Northampton', 'Reading', 'Cheltenham', 'Oxford United', 'Burton Albion', 'Wycombe (Wycombe Wanderers)', 'Lincoln City', 'Port Vale',
                      'Wigan Athletic']

# ENG League Two
England_League_Two = ['Sutton United (Sutton Utd)', 'Accrington Stanley (Accrington Stan)', 'Milton Keynes Dons', 'Salford City', 'Morecambe (Morecambe FC)', 'Barrow (Barrow AFC)', 'Crawley Town (Crawley)',
                      'Gillingham (Gillingham FC)', 'Harrogate (Harrogate Town)', 'Crewe Alexandra', 'Mansfield (Mansfield Town)', 'Grimsby (Grimsby Town)', 'AFC Wimbledon', 'Swindon', 'Colchester (Colchester Utd)',
                      'Tranmere (Tranmere Rovers)', 'Bradford City', 'Doncaster (Doncaster Rovers)', 'Stockport (Stockport Cty)', 'Wrexham (Wrexham AFC)', 'Forest Green (Forest Green Rovers)', 'Newport County', 'Notts County',
                      'Walsall (Walsall FC)']

# SCO Premiership
Scotland_Premiership = ['Celtic (Celtic Glasgow)', 'Glasgow Rangers (Rangers)', 'Hibernian Hibs (Hibernian)', 'Heart of Midlothian Hearts (Heart of Midlothian FC)', 'Ross County', 'Motherwell',
                        'St Johnstone', 'Kilmarnock Killie (Kilmarnock)', 'Aberdeen', 'St Mirren', 'Dundee Dark Blues (Dundee)', 'Livingston']

# SCO Championship
Scotland_Championship = ['Dundee (Dundee Utd)', 'Greenock Morton (Greenock Morton FC)', 'Dunfermline (Dunfermline Athletic FC)', 'Queen`s Park (Queens Park)', 'Partick Thistle (Partick Thistle FC)', 'Raith Rovers', 'Inverness ( Inverness Caledonian Thistle FC)',
                         'Airdrieonians (Airdrieonians FC)', 'Ayr United (Ayr Utd)', 'Arbroath (Arbroath FC)']
# SCO League One
Scotland_League_One = ['Alloa Athletic', 'Falkirk', 'Hamilton (Hamilton Academical)', 'Queen of South (Queen of The South)', 'Stirling Albion (Stirling Albion FC)', 'Kelty Hearts (Kelty Hearts FC)', 'Cove Rangers (Cove Rangers FC)',
                         'Montrose', 'Edinburgh City']

# SCO League Two
Scotland_League_Two = ['Bonnyrigg Rose', 'Clyde (Clyde FC)', 'Dumbarton', 'East Fife (East Fife FC)', 'Elgin City', 'Forfar Athletic (Forfar Athletic FC)', 'Peterhead (Peterhead FC)', 'Stenhousemuir (Stenhousemuir FC)', 'Stranraer (Stranraer FC)', 'Spartans (Spartans FC)']



import pandas as pd

data = {
    'England-Premier League': English_Premier_League,
    'England-EFL Cup': English_Football_League,
    'England-League One': England_League_One,
    'England-League Two': England_League_Two,
    'Scotland-Premiership': Scotland_Premiership,
    'Scotland-Championship': Scotland_Championship,
    'Scotland-League One': Scotland_League_One,
    'Scotland-League Two': Scotland_League_Two
}

# Find the maximum length among all arrays
max_length = max(len(data[key]) for key in data)

for key in data:
    print(f'{key} {len(data[key])}')

# Pad the arrays to the same length with empty strings
for key in data:
    data[key] += [''] * (max_length - len(data[key]))

df = pd.DataFrame(data)
# Define a custom function to extract values within brackets
def extract_values(text):
    result = text.split('(')[-1].replace(')', '')
    return result

# Apply the custom function to all columns
df = df.applymap(extract_values)

# Define a custom function to extract values within brackets
def extract_values(text):
    if '(' in text and ')' in text:
        result = text.split('(')[-1].replace(')', '').strip()
    else:
        result = text.strip()
    return result

def return_df(df=None):
    # Apply the custom function to all columns
    df = df.applymap(extract_values)
    df.to_csv("betway.csv")

    return df

# print(df.columns)
if __name__ == '__main__':
    return_df(df)