# ENGLAND PREMIER LEAGUE
English_Premier_League = ['Arsenal (Arsenal FC)', 'Aston Villa', 'Bournemouth (AFC Bournemouth)', 'Brentford (Brentford FC)', 'Brighton & Hove Albion (Brighton & Hove Albion)', 'Burnley (Burnley FC)', 'Chelsea (Chelsea FC)' , 'Everton (Everton FC)',
                          'Crystal Palace', 'Fulham (Fulham FC)', 'Liverpool (Liverpool FC)', 'Luton Town', 'Manchester City', 'Manchester United ', 'Newcastle United',
                          'Nottingham Forest', 'Sheffield United ', 'Tottenham Hotspur', 'West Ham United', 'Wolverhampton Wanderers']


# ENGLAND Championship
English_Football_League = ['Birmingham City', 'Blackburn Rovers', 'Bristol City', 'Cardiff City ', 'Coventry City', 'Huddersfield Town',
                           'Hull City', 'Ipswich Town', 'Leeds United', 'Leicester City', 'Middlesbrough (Middlesbrough FC)', 'Millwall (Millwall FC)', 'Norwich City',
                           'Plymouth Argyle', 'Preston North End', 'Queens Park Rangers', 'Rotherham United', 'Sheffield Wednesday',
                           'Southampton (Southampton FC)', 'Stoke City', 'Sunderland (Sunderland AFC)' , 'Swansea City ', 'Watford (Watford FC)', 'West Bromwich Albion']

# ENGLAND League One
England_League_One = ['Barnsley', 'Bolton (Bolton Wanderers)', 'Exeter City', 'Blackpool', 'Cambridge United', 'Charlton (Charlton Athletic)', 'Peterborough (Peterborough United)', 'Shrewsbury (Shrewsbury Town)',
                      'Stevenage (Stevenage FC)', 'Portsmouth (Portsmouth FC)', 'Carlisle United', 'Fleetwood Town', 'Bristol Rovers', 'Derby County', 'Leyton Orient London',
                      'Northampton (Northampton Town)', 'Reading (Reading FC)', 'Cheltenham (Cheltenham Town)', 'Oxford United', 'Burton Albion', 'Wycombe (Wycombe Wanderers)', 'Lincoln City', 'Port Vale',
                      'Wigan Athletic']

# ENGLAND League Two
England_League_Two = ['Sutton United', 'Accrington Stanley', 'Milton Keynes Dons', 'Salford City', 'Morecambe (Morecambe FC)', 'Barrow (Barrow AFC)', 'Crawley Town',
                      'Gillingham (Gillingham FC)', 'Harrogate (Harrogate Town)', 'Crewe Alexandra', 'Mansfield (Mansfield Town)', 'Grimsby (Grimsby Town)', 'AFC Wimbledon', 'Swindon (Swindon Town)', 'Colchester (Colchester United)',
                      'Tranmere (Tranmere Rovers FC)', 'Bradford City', 'Doncaster (Doncaster Rovers)', 'Stockport (Stockport County FC)', 'Wrexham (Wrexham AFC)', 'Forest Green (Forest Green Rovers)', 'Newport County', 'Notts County',
                      'Walsall (Walsall FC)']


# SCOTLAND Premiership
Scotland_Premiership = ['Celtic (Celtic Glasgow)', 'Glasgow Rangers', 'Hibernian Hibs (Hibernian FC)', 'Heart of Midlothian Hearts (Heart of Midlothian FC)', 'Ross County (Ross County FC)', 'Motherwell (Motherwell FC)',
                        'St Johnstone (St Johnstone FC)', 'Kilmarnock Killie (Kilmarnock FC)', 'Aberdeen (Aberdeen FC)', 'St Mirren (St Mirren FC)', 'Dundee Dark Blues (FC Dundee)', 'Livingston (Livingston FC)']

# SCOTLAND Championship
Scotland_Championship = ['Dundee (Dundee United)', 'Greenock Morton (Greenock Morton FC)', 'Dunfermline (Dunfermline Athletic FC)', 'Queen`s Park (Queens Park FC)', 'Partick Thistle (Partick Thistle FC)', 'Raith Rovers (Raith Rovers FC)', 'Inverness (Inverness Caledonian Thistle FC)',
                         'Airdrieonians (Airdrieonians FC)', 'Ayr United (Ayr United FC)', 'Arbroath (Arbroath FC)']
# SCOTLAND League One
Scotland_League_One = ['Alloa Athletic (Alloa Athletic FC)', 'Falkirk (Falkirk FC)', 'Hamilton (Hamilton Academical FC)', 'Queen of South (Queen of The South FC)', 'Stirling Albion (Stirling Albion FC)', 'Kelty Hearts (Kelty Hearts FC)', 'Cove Rangers (Cove Rangers FC)',
                         'Montrose (Montrose FC)', 'Edinburgh City (Edinburgh City FC)']

# Scotland -League Two
Scotland_League_Two = ['Bonnyrigg Rose', 'Clyde FC', 'Dumbarton FC', 'East Fife FC', 'Elgin City FC', 'Forfar Athletic FC', 'Peterhead FC', 'Stenhousemuir FC', 'Stranraer FC', 'Spartans FC']



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
    df.to_csv("betking.csv")

    return df

# print(df.columns)
if __name__ == '__main__':
    return_df(df)