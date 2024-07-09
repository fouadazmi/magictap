from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Replace 'sqlite:///users.db' with your actual database URL if different
DATABASE_URL = 'sqlite:///instance/users.db'

# Create an engine and connect to the database
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflect all tables
metadata.reflect(bind=engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Print all tables
print("Tables in the database:")
for table in metadata.tables.keys():
    print(table)

# Print data from each table
for table_name, table in metadata.tables.items():
    print(f"\nData in table '{table_name}':")
    select_stmt = table.select()
    result = session.execute(select_stmt)
    for row in result:
        print(row)

# Close the session
session.close()
