import psycopg2

def get_connection():
    conn = psycopg2.connect('postgresql://quotes_db_zb2f_user:tFp9kNbdMeQ62DK95FIQi8LSsYwABLmH@dpg-d8p8hmpo3t8c73ef1cmg-a.frankfurt-postgres.render.com/quotes_db_zb2f')
    return conn