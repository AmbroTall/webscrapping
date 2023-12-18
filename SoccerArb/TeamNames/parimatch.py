# ENGLAND PREMIER LEAGUE
English_Premier_League = ['Arsenal FC', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton', 'Burnley', 'Chelsea' , 'Everton',
                              'Crystal Palace', 'Fulham', 'Liverpool', 'Luton Town', 'Man City', 'Man Utd ', 'Newcastle',
                          'Nottm Forest', 'Sheff Utd ', 'Tottenham', 'West Ham', 'Wolverhampton ']


# ENGLAND Championship
English_Football_League = ['Birmingham', 'Blackburn', 'Bristol City', 'Cardiff ', 'Coventry ', 'Huddersfield',
                               'Hull', 'Ipswich Town', 'Leeds', 'Leicester', 'Middlesbrough', 'Millwall', 'Norwich',
                           'Plymouth', 'Preston', 'QPR', 'Rotherham', 'Sheff Wed',
                           'Southampton', 'Stoke', 'Sunderland' , 'Swansea', 'Watford', 'West Brom']

# ENGLAND League One
England_League_One = ['Barnsley', 'Bolton ', 'Exeter City', 'Blackpool', 'Cambridge Utd', 'Charlton ', 'Peterborough ', 'Shrewsbury ',
                      'Stevenage ', 'Portsmouth', 'Carlisle', 'Fleetwood Town', 'Bristol Rovers', 'Derby ', 'Leyton Orient',
                      'Northampton', 'Reading', 'Cheltenham', 'Oxford Utd', 'Burton Albion', 'Wycombe Wanderers FC', 'Lincoln City', 'Port Vale',
                      'Wigan ']

# ENGLAND League Two
England_League_Two = ['Sutton Utd', 'Accrington Stanley', 'Milton Keynes Dons', 'Salford City', 'Morecambe', 'Barrow A.F.C. ', 'Crawley Town',
                      'Gillingham', 'Harrogate (Harrogate Town)', 'Crewe Alexandra ', 'Mansfield Town', 'Grimsby', 'AFC Wimbledon', 'Swindon', 'Colchester',
                      'Tranmere', 'Bradford City AFC', 'Doncaster Rovers', 'Stockport County', 'Wrexham', 'Forest Green Rovers', 'Newport County', 'Notts County',
                      'Walsall ']


# SCOTLAND Premiership
Scotland_Premiership = ['Celtic', 'Rangers', 'Hibernian', 'Hearts', 'Ross County', 'Motherwell ',
                        'St Johnstone ', 'Kilmarnock', 'Aberdeen', 'St Mirren', 'Dundee FC', 'Livingston']

# SCOTLAND Championship
Scotland_Championship = ['Dundee (Dundee Utd)', 'Greenock Morton', 'Dunfermline Athletic', "Queen`s Park (Queens Park)", 'Partick', 'Raith Rovers', 'Inverness CT',
                         'Airdrieonians FC', 'Ayr United', 'Arbroth']
# SCOTLAND League One
Scotland_League_One = ['Alloa Athletic', 'Falkirk', 'Hamilton (Hamilton Academical)', 'Queen of the South', 'Stirling Albion', 'Kelty Hearts', 'Cove Rangers',
                         'Montrose', 'FC Edinburgh ']

# Scotland -League Two
Scotland_League_Two = ['Bonnyrigg Rose Athletic', 'Clyde', 'Dumbarton FC', 'East Fife', 'Elgin City', 'Forfar Athletic FC', 'Peterhead', 'Stenhousemuir', 'Stranraer', 'Spartans']


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
    df.to_csv("parimatch.csv")

    return df

# print(df.columns)
if __name__ == '__main__':
    return_df(df)