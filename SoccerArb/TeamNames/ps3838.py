# England-Premier League
English_Premier_League = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton and Hove Albion', 'Burnley', 'Chelsea', 'Everton',
                          'Crystal Palace', 'Fulham', 'Liverpool', 'Luton Town', 'Manchester City', 'Manchester United', 'Newcastle United',
                          'Nottingham Forest', 'Sheffield United', 'Tottenham Hotspur', 'West Ham United', 'Wolverhampton Wanderers (Wolves)']


# England-EFL Cup
English_Football_League = ['Birmingham City', 'Blackburn Rovers', 'Bristol City', 'Cardiff City', 'Coventry', 'Huddersfield Town',
                           'Hull City', 'Ipswich Town', 'Leeds United', 'Leicester City', 'Middlesbrough', 'Millwall', 'Norwich City',
                           'Plymouth Argyle', 'Preston North End (Preston)', 'Queens Park Rangers', 'Rotherham United (Rotherham)', 'Sheffield Wednesday',
                           'Southampton', 'Stoke City', 'Sunderland', 'Swansea City', 'Watford', 'West Bromwich Albion (West Brom)']

# England-League One
England_League_One = ['Barnsley', 'Bolton Wanderers', 'Exeter City', 'Blackpool', 'Cambridge United', 'Charlton', 'Peterborough United', 'Shrewsbury',
                      'Stevenage', 'Portsmouth', 'Carlisle United (Carlisle)', 'Fleetwood Town', 'Bristol Rovers', 'Derby County', 'Leyton Orient',
                      'Northampton (Northampton Town)', 'Reading', 'Cheltenham (Cheltenham Town)', 'Oxford United', 'Burton Albion', 'Wycombe', 'Lincoln City', 'Port Vale',
                      'Wigan Athletic']

# England-League Two
England_League_Two = ['Sutton United', 'Accrington Stanley', 'MK Dons', 'Salford City', 'Morecambe', 'Barrow', 'Crawley Town',
                      'Gillingham', 'Harrogate Town', 'Crewe Alexandra ', 'Mansfield ', 'Grimsby', 'AFC Wimbledon ', 'Swindon', 'Colchester (Colchester United)',
                      'Tranmere Rovers', 'Bradford City', 'Doncaster ', 'Stockport', 'Wrexham', 'Forest Green (Forest Green Rovers)', 'Newport County', 'Notts County',
                      'Walsall']



# Scotland-Premiership ****
Scotland_Premiership = ['Celtic', 'Glasgow Rangers (Rangers)', 'Hibernian Hibs (Hibernian)', 'Heart of Midlothian Hearts (Hearts)', 'Ross County', 'Motherwell',
                        'St Johnstone', 'Kilmarnock Killie (Kilmarnock)', 'Aberdeen', 'St Mirren', 'Dundee Dark Blues (Dundee)', 'Livingston']

# # Scotland-Championship
# Scotland_Championship = ['Dundee (Dundee Utd)', 'Greenock Morton', 'Dunfermline', 'Queen`s Park (Queens Park)', 'Partick Thistle', 'Raith Rovers', 'Inverness',
#                          'Airdrieonians (Airdrie)', 'Ayr United (Ayr Utd)', 'Arbroath']
# # Scotland-League One
# Scotland_League_One = ['Alloa Athletic', 'Falkirk', 'Hamilton', 'Queen of South', 'Stirling Albion', 'Kelty Hearts', 'Cove Rangers',
#                          'Montrose', 'Edinburgh City']
#
# # Scotland -League Two
# Scotland_League_Two = ['Bonnyrigg Rose', 'Clyde', 'Dumbarton', 'East Fife', 'Elgin City', 'Forfar Athletic', 'Peterhead', 'Stenhousemuir', 'Stranraer', 'Spartans']



import pandas as pd

data = {
    'England-Premier League': English_Premier_League,
    'England-EFL Cup': English_Football_League,
    'England-League One': England_League_One,
    'England-League Two': England_League_Two,
    'Scotland-Premiership': Scotland_Premiership,
    'Scotland-Championship': [],
    'Scotland-League One': [],
    'Scotland-League Two': []
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
        result = text.split('(')[-1].replace(')', '')
    else:
        result = text
    return result

def return_df(df=None):
    # Apply the custom function to all columns
    df = df.applymap(extract_values)
    df.to_csv("ps3838.csv")
    return df

# print(df.columns)
if __name__ == '__main__':
    return_df(df)