# ENGLAND PREMIER LEAGUE
English_Premier_League = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton', 'Burnley', 'Chelsea' , 'Everton',
                          'Crystal Palace', 'Fulham', 'Liverpool', 'Luton', 'Manchester City', 'Manchester United ', 'Newcastle United',
                          'Nottingham Forest', 'Sheffield United ', 'Tottenham', 'West Ham', 'Wolverhampton']


# ENGLAND Championship
English_Football_League = ['Birmingham', 'Blackburn', 'Bristol City', 'Cardiff ', 'Coventry ', 'Huddersfield',
                           'Hull City', 'Ipswich', 'Leeds United', 'Leicester', 'Middlesbrough', 'Millwall', 'Norwich ',
                           'Plymouth', 'Preston', 'QPR', 'Rotherham', 'Sheffield Wednesday',
                           'Southampton', 'Stoke City', 'Sunderland' , 'Swansea  ', 'Watford', 'West Bromwich Albion']

# ENGLAND League One
England_League_One = ['Barnsley', 'Bolton', 'Exeter City FC', 'Blackpool', 'Cambridge United', 'Charlton ', 'Peterborough ', 'Shrewsbury',
                      'Stevenage (Stevenage FC)', 'Portsmouth', 'Carlisle United', 'Fleetwood Town', 'Bristol Rovers', 'Derby ', 'Leyton Orient',
                      'Northampton (Northampton Town)', 'Reading', 'Cheltenham', 'Oxford United', 'Burton Albion', 'Wycombe', 'Lincoln City', 'Port Vale',
                      'Wigan']

# ENGLAND League Two
England_League_Two = ['Sutton United', 'Accrington Stanley', 'Milton Keynes Dons', 'Salford City', 'Morecambe (Morecambe FC)', 'Barrow ', 'Crawley Town',
                      'Gillingham (Gillingham FC)', 'Harrogate (Harrogate Town)', 'Crewe ', 'Mansfield (Mansfield Town)', 'Grimsby (Grimsby)', 'AFC Wimbledon', 'Swindon (Swindon Town)', 'Colchester (Colchester United)',
                      'Tranmere', 'Bradford City', 'Doncaster', 'Stockport', 'Wrexham', 'Forest Green', 'Newport County', 'Notts County',
                      'Walsall ']


# SCOTLAND Premiership
Scotland_Premiership = ['Celtic', 'Rangers', 'Hibernian', 'Hearts', 'Ross County', 'Motherwell ',
                        'St Johnstone ', 'Kilmarnock', 'Aberdeen', 'St Mirren FC', 'Dundee', 'Livingston']

# SCOTLAND Championship
Scotland_Championship = ['Dundee (Dundee United)', 'Greenock Morton', 'Dunfermline', "Queen`s Park (Queen's Park)", 'Partick Thistle ', 'Raith', 'Inverness',
                         'Airdrieonians', 'Ayr United', 'Arbroath (Arbroath FC)']
# SCOTLAND League One
Scotland_League_One = ['Alloa', 'Falkirk', 'Hamilton (Hamilton Academical)', 'Queen Of South', 'Stirling Albion', 'Kelty Hearts', 'Cove Rangers',
                         'Montrose', 'Edinburgh City (Edinburgh City)']

# Scotland -League Two
Scotland_League_Two = ['Bonnyrigg Rose', 'Clyde', 'Dumbarton', 'East Fife', 'Elgin City', 'Forfar Athletic', 'Peterhead', 'Stenhousemuir FC', 'Stranraer', 'Spartans']



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
        result = text.split('(')[-1].replace(')', '')
    else:
        result = text
    return result

def return_df(df=None):
    # Apply the custom function to all columns
    df = df.applymap(extract_values)
    df.to_csv("betbonanza.csv")

    return df

# print(df.columns)
if __name__ == '__main__':
    return_df(df)