from variables import today
import psycopg2 as db

from prefect.blocks.system import Secret
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

tabla = 'btc_valores'


def _connect_db(password):
    try:
        conn = db.connect(
            host= DB_HOST,
            user= DB_USER,
            password = password,
            database=DB_NAME,
            port= DB_NAME ,
        )
        return conn
    except OperationalError as e:
        print(e)

def _row_validate(curs):
    query_exists = f"SELECT fecha FROM {tabla} WHERE fecha = '{str(today)}'"
    curs.execute(query_exists)
    row = curs.fetchone()
    assert not row, f'Ya existe un registro para el dia {today}'


def _create_table(tablon, conn, curs):
    try:
        cols_name = [col for col in tablon.columns]
        cols_types = ["DECIMAL(20,2)", "DECIMAL(20,2)", "DECIMAL(20,2)", "VARCHAR"]
        cols_definitions = [
            f"{name} {cols_types[i % 4]}" for i, name in enumerate(cols_name)
        ]

        query_table = f'''
            CREATE TABLE IF NOT EXISTS btc_valores (
                fecha DATE PRIMARY KEY,
                {', '.join(cols_definitions)}
            )
        '''
        curs.execute(query_table)
        conn.commit()
    except OperationalError as e:
        print(e)

def _insert_row(tablon, conn, curs):
    try:
        tablon = tablon.reset_index()
        # Crea los placeholders (%s, %s, ...) según la cantidad de columnas
        placeholders = ', '.join(['%s'] * tablon.shape[1])
        sql = f'INSERT INTO {tabla} VALUES ({placeholders})'
        # Convertir el DataFrame en una lista de tuplas y ejecutar en batch
        data = [tuple(row) for row in tablon.itertuples(index=False, name=None)][0]
        curs.execute(sql, data)
        conn.commit()
    except OperationalError as e:
        print(e)

def load_tablon(tablon):
    try:
        assert not len(tablon.index) != 1, f'NASDAQ no ha operado en el dia de la fecha {today}'
        # congifurar para que los Secret sean buscado en PrefectCloud, 
        # configuracion por default busca el Secret en local 
        #  credentials = Secret.load('nombre_elegido_en_prefect_cloud') # usar para ejecuvion en la nube
        password = DB_PASSWORD, # usar en entorno local
        conn = _connect_db(password)
        if conn is not None:
            curs = conn.cursor()
            _create_table(tablon, conn, curs)
            _row_validate(curs)
            _insert_row(tablon, conn, curs)
            curs.close()
            conn.close()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    pass
    # from extract import get_raw_dict
    # from transform import get_tablon
    # raw_dict = get_raw_dict()
    # tablon = get_tablon(raw_dict)
    # load_tablon(tablon)