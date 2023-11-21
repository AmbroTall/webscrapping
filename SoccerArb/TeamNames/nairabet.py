# ENGLAND PREMIER LEAGUE
English_Premier_League = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton & Hove Albion (Brighton)', 'Burnley', 'Chelsea' , 'Everton',
                          'Crystal Palace', 'Fulham', 'Liverpool', 'Luton Town (Luton)', 'Manchester City (Man City)', 'Manchester United (Man Utd)', 'Newcastle United (Newcastle)',
                          'Nottingham Forest', 'Sheffield United (Sheffield Utd)', 'Tottenham Hotspur (Spurs)', 'West Ham United (West Ham)', 'Wolverhampton Wanderers (Wolves)']


# ENGLAND Championship
English_Football_League = ['Birmingham City (Birmingham)', 'Blackburn Rovers (Blackburn)', 'Bristol City', 'Cardiff City (Cardiff)', 'Coventry City (Coventry)' , 'Huddersfield Town (Huddersfield)',
                           'Hull City (Hull)', 'Ipswich Town (Ipswich)', 'Leeds United (Leeds)', 'Leicester City (Leicester)', 'Middlesbrough', 'Millwall', 'Norwich City (Norwich)',
                           'Plymouth Argyle (Plymouth)', 'Preston North End (Preston)', 'Queens Park Rangers (QPR)', 'Rotherham United (Rotherham)', 'Sheffield Wednesday',
                           'Southampton', 'Stoke City (Stoke)', 'Sunderland' , 'Swansea City (Swansea)', 'Watford', 'West Bromwich Albion (West Brom)']

# ENGLAND League One
England_League_One = ['Barnsley', 'Bolton', 'Exeter City (Exeter)' , 'Blackpool', 'Cambridge United (Cambridge Utd)', 'Charlton', 'Peterborough ', 'Shrewsbury',
                      'Stevenage ', 'Portsmouth ', 'Carlisle United (Carlisle)', 'Fleetwood Town  (Fleetwood)', 'Bristol Rovers', 'Derby County (Derby)', 'Leyton Orient London (Leyton Orient)',
                      'Northampton', 'Reading', 'Cheltenham', 'Oxford United (Oxford Utd)', 'Burton Albion (Burton)', 'Wycombe', 'Lincoln City (Lincoln)', 'Port Vale',
                      'Wigan Athletic (Wigan)']

# ENGLAND League Two
England_League_Two = ['Sutton United', 'Accrington Stanley (Accrington)', 'Milton Keynes Dons (MK Dons)', 'Salford City', 'Morecambe', 'Barrow', 'Crawley Town (Crawley)',
                      'Gillingham ', 'Harrogate (Harrogate Town)', 'Crewe Alexandra (Crewe)', 'Mansfield', 'Grimsby', 'AFC Wimbledon', 'Swindon', 'Colchester',
                      'Tranmere', 'Bradford City (Bradford)', 'Doncaster', 'Stockport', 'Wrexham', 'Forest Green (Forest Green Rovers)', 'Newport County', 'Notts County',
                      'Walsall']


# SCOTLAND Scottish Premiership
Scotland_Premiership = ['Celtic', 'Glasgow Rangers (Rangers)', 'Hibernian Hibs (Hibernian)', 'Heart of Midlothian Hearts (Heart of Midlothian)', 'Ross County', 'Motherwell',
                        'St Johnstone (St. Johnstone)', 'Kilmarnock Killie (Kilmarnock)', 'Aberdeen', 'St Mirren', 'Dundee Dark Blues (Dundee)', 'Livingston']

# SCOTLAND Scottish Championship
Scotland_Championship = ['Dundee (Dundee United)', 'Greenock Morton (Morton)', 'Dunfermline', "Queen`s Park (Queen's Park)", 'Partick Thistle (Partick Thistle)', 'Raith Rovers', 'Inverness (Inverness Caledonian Thistle)',
                         'Airdrieonians (Airdrie Utd)', 'Ayr United (Ayr)', 'Arbroath']
# SCOTLAND Scottish League One
Scotland_League_One = ['Alloa Athletic (Alloa)', 'Falkirk', 'Hamilton (Hamilton Academical)', 'Queen of South', 'Stirling Albion', 'Kelty Hearts', 'Cove Rangers (Cove Rangers FC)',
                         'Montrose', 'Edinburgh City']

# Scotland -League Two
Scotland_League_Two = ['Bonnyrigg Rose', 'Clyde', 'Dumbarton ', 'East Fife', 'Elgin', 'Forfar', 'Peterhead', 'Stenhousemuir', 'Stranraer', 'Spartans']



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
    df.to_csv("nairabet.csv")

    return df

# print(df.columns)
if __name__ == '__main__':
    return_df(df)
