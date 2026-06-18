import psycopg2
conn = psycopg2.connect('postgresql://quotes_db_zb2f_user:tFp9kNbdMeQ62DK95FIQi8LSsYwABLmH@dpg-d8p8hmpo3t8c73ef1cmg-a.frankfurt-postgres.render.com/quotes_db_zb2f')
cursor = conn.cursor()

import psycopg2

conn = psycopg2.connect('postgresql://quotes_db_zb2f_user:tFp9kNbdMeQ62DK95FIQi8LSsYwABLmH@dpg-d8p8hmpo3t8c73ef1cmg-a.frankfurt-postgres.render.com/quotes_db_zb2f')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS QUOTES (
        Id SERIAL PRIMARY KEY,
        Quote_id VARCHAR(50),
        Quote_number VARCHAR(50),
        Customer_Id VARCHAR(50),
        Vehicle_id VARCHAR(50),
        description_Q VARCHAR(255),
        created_by VARCHAR(100)
    )
''')
conn.commit()
print('Table created!')

# Insert data
cursor.execute('''
    INSERT INTO QUOTES (Quote_id, Quote_number, Customer_Id, Vehicle_id, description_Q, created_by)
    VALUES 
    (%s, %s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s, %s)
''', (
    'Q001', 'QN-001', 'CUST-01', 'BENZ001', None, None,
    'Q002', 'QN-002', 'CUST-02', 'BENZ002', 'Brake problems', 'Rorisang',
    'Q003', 'QN-003', 'CUST-04', 'BENZ003', 'Brake problems', 'Rorisang'
    
))
conn.commit()
print('Data inserted!')

# Creating line items table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS line_items (
        id SERIAL PRIMARY KEY,
        quote_id INTEGER REFERENCES quotes(id),
        description VARCHAR(255),
        quantity INTEGER,
        unit_price DECIMAL(10,2),
        total DECIMAL(10,2)
    )
''')
print('Line item table created')
