# ENGLAND PREMIER LEAGUE
English_Premier_League = ['Arsenal (Arsenal FC)', 'Aston Villa', 'Bournemouth (Bournemouth AFC)', 'Brentford (Brentford FC)', 'Brighton & Hove Albion', 'Burnley (Burnley FC)', 'Chelsea (Chelsea FC)' , 'Everton',
                          'Crystal Palace', 'Fulham (Fulham FC)', 'Liverpool (Liverpool FC)', 'Luton Town', 'Manchester City', 'Manchester United ', 'Newcastle United',
                          'Nottingham Forest', 'Sheffield United (Sheffield Utd)', 'Tottenham Hotspur', 'West Ham United', 'Wolverhampton Wanderers']


# ENGLAND Championship
English_Football_League = ['Birmingham City', 'Blackburn Rovers', 'Bristol City', 'Cardiff City ', 'Coventry City', 'Huddersfield Town',
                           'Hull City', 'Ipswich Town', 'Leeds United', 'Leicester City', 'Middlesbrough (Middlesbrough FC)', 'Millwall (Millwall FC)', 'Norwich City',
                           'Plymouth Argyle', 'Preston North End', 'Queens Park Rangers', 'Rotherham United (Rotherham Utd)', 'Sheffield Wednesday',
                           'Southampton', 'Stoke City', 'Sunderland (Sunderland AFC)' , 'Swansea City ', 'Watford', 'West Bromwich Albion']

# ENGLAND League One
England_League_One = ['Barnsley (Barnsley FC)', 'Bolton (Bolton Wanderers)', 'Exeter City', 'Blackpool (Blackpool FC)', 'Cambridge United (Cambridge Utd FC)', 'Charlton (Charlton Athletic)', 'Peterborough (Peterborough United)', 'Shrewsbury (Shrewsbury Town)',
                      'Stevenage (Stevenage FC)', 'Portsmouth (Portsmouth FC)', 'Carlisle United (Carlisle Utd)', 'Fleetwood Town', 'Bristol Rovers', 'Derby County', 'Leyton Orient London (Leyton Orient)',
                      'Northampton (Northampton Town)', 'Reading (Reading FC)', 'Cheltenham (Cheltenham Town)', 'Oxford United', 'Burton Albion', 'Wycombe (Wycombe Wanderers)', 'Lincoln City', 'Port Vale (Port Vale FC)',
                      'Wigan Athletic']

# ENGLAND League Two
England_League_Two = ['Sutton United (Sutton Utd)', 'Accrington Stanley', 'Milton Keynes Dons', 'Salford City', 'Morecambe (Morecambe FC)', 'Barrow (Barrow FC)', 'Crawley Town',
                      'Gillingham ', 'Harrogate (Harrogate Town)', 'Crewe Alexandra (Crewe Alexandra FC)', 'Mansfield (Mansfield Town)', 'Grimsby (Grimsby Town)', 'AFC Wimbledon (Wimbledon)', 'Swindon (Swindon Town)', 'Colchester (Colchester United)',
                      'Tranmere (Tranmere Rovers FC)', 'Bradford City', 'Doncaster (Doncaster Rovers)', 'Stockport (Stockport County)', 'Wrexham (Wrexham FC)', 'Forest Green (Forest Green Rovers)', 'Newport County', 'Notts County',
                      'Walsall']


# SCOTLAND Scottish Premiership
Scotland_Premiership = ['Celtic (Celtic FC)', 'Glasgow Rangers (Rangers FC)', 'Hibernian Hibs (Hibernian FC)', 'Heart of Midlothian Hearts (Heart of Midlothian)', 'Ross County (Ross County FC)', 'Motherwell (Motherwell FC)',
                        'St Johnstone ', 'Kilmarnock Killie (Kilmarnock FC)', 'Aberdeen (Aberdeen FC)', 'St Mirren (FC St Mirren)', 'Dundee Dark Blues (Dundee FC)', 'Livingston (Livingston FC)']

# SCOTLAND Scottish Championship
Scotland_Championship = ['Dundee (Dundee United)', 'Greenock Morton', 'Dunfermline (Dunfermline Athletic)', 'Queen`s Park (Queens Park FC)', 'Partick Thistle (Partick Thistle)', 'Raith Rovers (Raith Rovers FC)', 'Inverness (Inverness Caledonian Thistle)',
                         'Airdrieonians (Airdrie Utd)', 'Ayr United', 'Arbroath (Arbroath FC)']
# SCOTLAND Scottish League One
Scotland_League_One = ['Alloa Athletic (Alloa Athletic FC)', 'Falkirk (Falkirk FC)', 'Hamilton (Hamilton Academical)', 'Queen of South (Queen of The South FC)', 'Stirling Albion', 'Kelty Hearts (Kelty Hearts F.c.)', 'Cove Rangers (Cove Rangers FC)',
                         'Montrose (Montrose FC)', 'Edinburgh City']

# Scotland -League Two
Scotland_League_Two = ['Bonnyrigg Rose', 'Clyde (Clyde FC)', 'Dumbarton (Dumbarton FC)', 'East Fife (East Fife FC)', 'Elgin City', 'Forfar Athletic ', 'Peterhead (Peterhead FC)', 'Stenhousemuir (Stenhousemuir FC)', 'Stranraer (Stranraer FC)', 'Spartans (Spartans FC)']






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
    df.to_csv("merrybet.csv")

    return df

# print(df.columns)
if __name__ == '__main__':
    return_df(df)