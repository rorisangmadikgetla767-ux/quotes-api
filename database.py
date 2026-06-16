import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=Madixx\\SQLEXPRESS;" 
        "DATABASE=Mydatabase;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )
    return conn