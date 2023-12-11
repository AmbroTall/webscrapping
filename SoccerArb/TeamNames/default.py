English_Premier_League = ['Arsenal', 'Aston Villa', 'Bournemoth', 'Brentford', 'Brighton & Hove Albion', 'Burnley', 'Chelsea', 'Everton',
                          'Crystal Palace', 'Fulham', 'Liverpool', 'Luton Town', 'Manchester City', 'Manchester United', 'Newcastle United',
                          'Nottingham Forest', 'Sheffield United', 'Tottenham Hotspur', 'West Ham United', 'Wolverhampton Wanderers']

English_Championship = ['Birmingham City', 'Blackburn Rovers', 'Bristol City', 'Cardiff City', 'Coventry City', 'Huddersfield Town',
                           'Hull City', 'Ipswich Town', 'Leeds United', 'Leicester City', 'Middlesbrough', 'Millwall', 'Norwich City',
                           'Plymouth Argyle', 'Preston North End', 'Queens Park Rangers QPR', 'Rotherham United', 'Sheffield Wednesday',
                           'Southampton', 'Stoke City', 'Sunderland', 'Swansea City', 'Watford', 'West Bromwich Albion']

England_League_One = ['Barnsley', 'Bolton', 'Exeter City', 'Blackpool', 'Cambridge United', 'Charlton', 'Peterborough', 'Shrewsbury',
                      'Stevenage', 'Portsmouth', 'Carlisle United', 'Fleetwood Town', 'Bristol Rovers', 'Derby County', 'Leyton Orient',
                      'Northampton', 'Reading', 'Cheltenham', 'Oxford United', 'Burton Albion', 'Wycombe', 'Lincoln City', 'Port Vale',
                      'Wigan Athletic']

England_League_Two = ['Sutton United', 'Accrington Stanley', 'Milton Keynes Dons', 'Salford City', 'Morecambe', 'Barrow', 'Crawley Town',
                      'Gillingham', 'Harrogate', 'Crewe Alexandra', 'Mansfield', 'Grimsby', 'AFC Wimbledon', 'Swindon', 'Colchester',
                      'Tranmere', 'Bradford City', 'Doncaster', 'Stockport', 'Wrexham', 'Forest Green', 'Newport County', 'Notts County',
                      'Walsall']

Scotland_Premiership = ['Celtic', 'Glasgow Rangers', 'Hibernian Hibs', 'Heart of Midlothian Hearts', 'Ross County', 'Motherwell',
                        'St Johnstone', 'Kilmarnock Killie', 'Aberdeen', 'St Mirren', 'Dundee Dark Blues', 'Livingston']

Scotland_Championship = ['Dundee', 'Greenock Morton', 'Dunfermline', 'Queen`s Park', 'Partick Thistle', 'Raith Rovers', 'Inverness',
                         'Airdrieonians', 'Ayr United', 'Arbroath']

Scotland_League_One = ['Alloa Athletic', 'Falkirk', 'Hamilton', 'Queen of South', 'Stirling Albion', 'Kelty Hearts', 'Cove Rangers',
                         'Montrose', 'Edinburgh City']

Scotland_League_Two = ['Bonnyrigg Rose', 'Clyde (Clyde FC)', 'Dumbarton (Dumbarton FC)', 'East Fife (East Fife FC)', 'Elgin City (Elgin City FC)', 'Forfar Athletic (Forfar Athletic FC)', 'Peterhead (Peterhead FC)', 'Stenhousemuir (Stenhousemuir FC)', 'Stranraer (Stranraer FC)', 'Spartans (Spartans FC)']



import pandas as pd

data = {
    'England-Premier League': English_Premier_League,
    'England-EFL Cup': English_Championship,
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
    df.to_csv("default.csv")

    return df

# print(df.columns)
if __name__ == '__main__':
    return_df(df)
