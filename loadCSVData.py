import pandas as pd
from sqlalchemy import create_engine

# Specify your database credentials
user = 'root'
password = 'carrental..'
host = 'carrentalmanagementsystem.cp2we2aaom6h.us-east-2.rds.amazonaws.com'
port = '3306'
dbname = 'CarRentalDB'

# Create a connection string
conn_str = f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'

# Create an engine object
engine = create_engine(conn_str)

# Load your CSV file
df = pd.read_csv(r'C:/Users/ravin/OneDrive/Desktop/Advance Database Technologies/Week11/Final_Project_Part_2/CarRentalDataV1.csv')

# Load your CSV file with the specified delimiters and quoting characters
df = pd.read_csv(
    r'C:/Users/ravin/OneDrive/Desktop/Advance Database Technologies/Week11/Final_Project_Part_2/CarRentalDataV1.csv',
    delimiter=',',
    quotechar='"',
    lineterminator='\n'
)


df.columns = df.columns.str.strip() # remove the extra spaces in the column names

# Adjusting the column names suitable for StagingTable
df.columns = ['ownerId' if c == 'owner.id' else c for c in df.columns]
df.columns = [c.split('.')[-1] if c != 'rate.daily' else 'rateDaily' for c in df.columns]

# Transform the rating column by replacing empty strings with None (which converts to NULL in SQL)
df['rating'] = df['rating'].replace('', None)

# Insert data into the database
df.to_sql('StagingTable', con=engine, index=False, if_exists='append')
