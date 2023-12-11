# ENGLAND PREMIER LEAGUE
English_Premier_League = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton & Hove Albion (Brighton)', 'Burnley', 'Chelsea' , 'Everton',
                          'Crystal Palace', 'Fulham', 'Liverpool', 'Luton Town', 'Manchester City', 'Manchester United', 'Newcastle United',
                          'Nottingham Forest', 'Sheffield United', 'Tottenham Hotspur (Tottenham)', 'West Ham United (West Ham)', 'Wolverhampton Wanderers (Wolves)']

# ENGLAND Championship
English_Football_League = ['Birmingham City (Birmingham)', 'Blackburn Rovers', 'Bristol City', 'Cardiff City', 'Coventry City' , 'Huddersfield Town',
                           'Hull City', 'Ipswich Town', 'Leeds United', 'Leicester City', 'Middlesbrough', 'Millwall', 'Norwich City',
                           'Plymouth Argyle', 'Preston North End', 'Queens Park Rangers', 'Rotherham United', 'Sheffield Wednesday',
                           'Southampton', 'Stoke City', 'Sunderland' , 'Swansea City', 'Watford', 'West Bromwich Albion (West Bromwich)']

# ENGLAND League One
England_League_One = ['Barnsley', 'Bolton', 'Exeter City (Exeter)' , 'Blackpool', 'Cambridge United', 'Charlton (Charlton Athletic)', 'Peterborough (Peterborough United)', 'Shrewsbury (Shrewsbury Town)',
                      'Stevenage (Stevenage FC)', 'Portsmouth ', 'Carlisle United (Carlisle)', 'Fleetwood Town ', 'Bristol Rovers', 'Derby County', 'Leyton Orient London (Leyton Orient)',
                      'Northampton (Northampton Town)', 'Reading', 'Cheltenham', 'Oxford United', 'Burton Albion', 'Wycombe (Wycombe Wanderers)', 'Lincoln City', 'Port Vale',
                      'Wigan Athletic']

# ENGLAND League Two
England_League_Two = ['Sutton United', 'Accrington Stanley', 'Milton Keynes Dons', 'Salford City (Salford City FC)', 'Morecambe', 'Barrow', 'Crawley Town',
                      'Gillingham ', 'Harrogate (Harrogate Town)', 'Crewe Alexandra', 'Mansfield (Mansfield Town)', 'Grimsby (Grimsby Town)', 'AFC Wimbledon', 'Swindon (Swindon Town)', 'Colchester (Colchester United)',
                      'Tranmere (Tranmere Rovers)', 'Bradford City', 'Doncaster (Doncaster Rovers)', 'Stockport (Stockport County)', 'Wrexham', 'Forest Green (Forest Green Rovers)', 'Newport County', 'Notts County',
                      'Walsall']

# SCOTLAND Scottish Premiership
Scotland_Premiership = ['Celtic', 'Glasgow Rangers (Rangers FC)', 'Hibernian Hibs (Hibernian)', 'Heart of Midlothian Hearts (Hearts)', 'Ross County', 'Motherwell',
                        'St Johnstone ', 'Kilmarnock Killie (Kilmarnock)', 'Aberdeen', 'St Mirren', 'Dundee Dark Blues (Dundee FC)', 'Livingston']

# SCOTLAND Scottish Championship
Scotland_Championship = ['Dundee (Dundee United)', 'Greenock Morton', 'Dunfermline (Dunfermline Athletic)', "Queen`s Park (Queens Park Rangers)", 'Partick Thistle (Partick Thistle)', 'Raith Rovers', 'Inverness (Inverness CT)',
                         'Airdrieonians', 'Ayr United', 'Arbroath']

# Scotland-League One
Scotland_League_One = ['Alloa Athletic', 'Falkirk', 'Hamilton ( Hamilton Academical)', 'Queen of South (Queen of The South)', 'Stirling Albion', 'Kelty Hearts', 'Cove Rangers',
                         'Montrose', 'Edinburgh City (Edinburgh City)']

# Scotland -League Two
Scotland_League_Two = ['Bonnyrigg Rose Athletic', 'Clyde', 'Dumbarton', 'East Fife', 'Elgin City', 'Forfar Athletic', 'Peterhead', 'Stenhousemuir', 'Stranraer', 'Spartans (Spartans FC)']






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
    df.to_csv("sunbet.csv")
    return df

# print(df.columns)
if __name__ == '__main__':
    return_df(df)
