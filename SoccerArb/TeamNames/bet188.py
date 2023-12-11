# ENGLAND PREMIER LEAGUE
English_Premier_League = ['Arsenal', 'Aston Villa', 'AFC Bournemouth', 'Brentford', 'Brighton and Hove Albion', 'Burnley', 'Chelsea' , 'Everton',
                          'Crystal Palace', 'Fulham', 'Liverpool', 'Luton Town', 'Manchester City', 'Manchester United ', 'Newcastle United',
                          'Nottingham Forest', 'Sheffield United ', 'Tottenham Hotspur', 'West Ham United', 'Wolverhampton Wanderers']


# ENGLAND Championship
English_Football_League = ['Birmingham City', 'Blackburn Rovers', 'Bristol City', 'Cardiff City ', 'Coventry City ', 'Huddersfield Town',
                               'Hull City', 'Ipswich Town', 'Leeds United', 'Leicester City', 'Middlesbrough', 'Millwall', 'Norwich City ',
                           'Plymouth Argyle', 'Preston North End', 'Queens Park Rangers', 'Rotherham United', 'Sheffield Wednesday',
                           'Southampton', 'Stoke City', 'Sunderland' , 'Swansea City  ', 'Watford', 'West Bromwich Albion']

# ENGLAND League One
England_League_One = ['Barnsley', 'Bolton Wanderers', 'Exeter City', 'Blackpool', 'Cambridge United', 'Charlton Athletic ', 'Peterborough United ', 'Shrewsbury Town',
                          'Stevenage ', 'Portsmouth', 'Carlisle United', 'Fleetwood Town', 'Bristol Rovers', 'Derby County ', 'Leyton Orient',
                      'Northampton (Northampton Town)', 'Reading', 'Cheltenham Town', 'Oxford United', 'Burton Albion', 'Wycombe Wanderers', 'Lincoln City', 'Port Vale',
                      'Wigan Athletic']

# ENGLAND League Two
England_League_Two = ['Sutton United', 'Accrington Stanley', 'Milton Keynes Dons', 'Salford City', 'Morecambe', 'Barrow AFC', 'Crawley Town',
                      'Gillingham', 'Harrogate (Harrogate Town)', 'Crewe Alexandra ', 'Mansfield (Mansfield Town)', 'Grimsby (Grimsby Town)', 'AFC Wimbledon', 'Swindon (Swindon Town)', 'Colchester (Colchester United)',
                      'Tranmere Rovers', 'Bradford City', 'Doncaster Rovers', 'Stockport County', 'Wrexham', 'Forest Green Rovers', 'Newport County AFC', 'Notts County',
                      'Walsall']


# SCOTLAND Premiership
Scotland_Premiership = ['Celtic', 'Glasgow Rangers', 'Hibernian', 'Heart of Midlothian', 'Ross County', 'Motherwell ',
                        'St Johnstone ', 'Kilmarnock', 'Aberdeen', 'St Mirren', 'Dundee', 'Livingston']

# SCOTLAND Championship
Scotland_Championship = ['Dundee (Dundee United)', 'Greenock Morton', 'Dunfermline Athletic', "Queen`s Park (Queen's Park)", 'Partick Thistle ', 'Raith Rovers', 'Inverness',
                         'Airdrieonians', 'Ayr United', 'Arbroath']
# SCOTLAND League One
Scotland_League_One = ['Alloa Athletic', 'Falkirk', 'Hamilton (Hamilton Academical)', 'Queen of the South', 'Stirling Albion', 'Kelty Hearts', 'Cove Rangers',
                         'Montrose', 'Edinburgh FC']

# Scotland -League Two
Scotland_League_Two = ['Bonnyrigg Rose', 'Clyde', 'Dumbarton', 'East Fife', 'Elgin City', 'Forfar Athletic', 'Peterhead', 'Stenhousemuir', 'Stranraer', 'Spartans']



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
    df.to_csv("bet188.csv")
    return df

# print(df.columns)
if __name__ == '__main__':
    return_df(df)