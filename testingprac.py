import sqlite3
import mysql.connector

data = {'name': '3407 Talking Leaves Trail, Gainesville, GA 30506', 'beds': '3', 'baths': '2', 'sqFt': '1,790', 'lot_size': '27,007', 'year_built': '2004', 'APN': '10-048 -000-036', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'Yes', 'owner_type': 'Individual', 'owner_status': 'Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '6 Years 2 Months', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$391,881', 'last_year ': '$416,268', 'properties': '6', 'avg_sale_price': '$278,864', 'days_on_market': '65', 'open_mortgages': '65', 'est_mortgage_balance': '$170,226', 'involuntary_liens': '2', 'total_involuntary_amt': '$5,949.37', 'public_record': '$187,000\n05/31/2017', 'MLS': '$187,000/est\n05/2017', 'est_equity': '$221,655', 'linked_properties': '0', 'monthly_rent': '$1,775', 'gross_yield': '5.44%', 'owner_1_name': '', 'owner_2_name': '', 'url': 'https://app.propstream.com/search/1742100292', 'phone_numbers': "['(770) 369-1649', '(207) 799-8312', '(678) 696-8438', '(770) 369-1648', '(207) 420-3797', '(770) 965-0351', '(770) 530-8032', '(770) 926-8945']", 'email_contacts': "['GACOWBURN@YAHOO.COM', 'GREGORYCOWBURN@GMAIL.COM', 'GREGERYCOWBURN@YAHOO.COM', 'GCOWBURN@COMCAST.NET', 'GRLYNN@COX.NET', 'GRLYNN@BELLSOUTH.NET', 'GRLYNN@HOME.COM', 'HARDYSHIBRIKA@YAHOO.COM', 'GERSONVILLAGRAN@HOTMAIL.COM', 'KNOWLES5375@BELLSOUTH.NET', 'KAREYCOWBURN@YAHOO.COM', 'LYNNCOWBURN@MINDSPRING.COM', 'BROOKEURSO@GMAIL.COM', 'GCOBURN@MAINE.RR.COM', 'GREG.COBURN@AWWR.COM', 'GREG.COBURN@AWWREM.COM']", 'truthfinder_url': 'https://www.truthfinder.com/dashboard/reports/3cf13dc7-d277-4c64-8661-efface1e42b1', 'ga_id': 2901499}


def save_data_to_databases(data):
    try:
        # Connect to the SQLite database or create a new one if it doesn't exist
        conn_sqlite = sqlite3.connect('property_data.db')
        cursor_sqlite = conn_sqlite.cursor()

        # Connect to the MySQL database
        conn_mysql = mysql.connector.connect(
            host='168.119.4.62',
            user='helixhel_oldcrawlersusr',
            password='NdSZIAfVZHoA',
            database='helixhel_oldcrawlersdb',
        )
        cursor_mysql = conn_mysql.cursor()

        # Remove any unused parameters from the data dictionary
        valid_columns = ['name', 'beds', 'baths', 'sqFt', 'lot_size', 'year_built', 'APN', 'property_type', 'status',
                         'distressed', 'short_scale', 'HOA_COA', 'owner_type', 'owner_status', 'occupancy',
                         'length_of_ownership', 'purchase_method', 'county', 'estimated_value', 'last_year',
                         'properties', 'avg_sale_price', 'days_on_market', 'open_mortgages', 'est_mortgage_balance',
                         'involuntary_liens', 'total_involuntary_amt', 'public_record', 'MLS', 'est_equity',
                         'linked_properties', 'monthly_rent', 'gross_yield', 'owner_1_name', 'owner_2_name', 'url',
                         'phone_numbers', 'email_contacts', 'truthfinder_url', 'ga_id']
        data = {k: v for k, v in data.items() if k in valid_columns}

        # Insert data into the SQLite table
        keys = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.keys()])
        values = tuple(data.values())
        query = f"INSERT INTO properties_two ({keys}) VALUES ({placeholders})"
        cursor_sqlite.execute(query, values)

        # Insert data into the MySQL table
        cursor_mysql.execute(query, values)

        # Commit the changes to SQLite and MySQL
        conn_sqlite.commit()
        conn_sqlite.close()
        conn_mysql.commit()
        conn_mysql.close()

        print("Data saved to both SQLite and MySQL successfully!")
    except (sqlite3.Error, mysql.connector.Error) as e:
        print("An error occurred while saving data:", str(e))

save_data_to_mysql(data)