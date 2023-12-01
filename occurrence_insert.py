import pandas as pd
import psycopg2 
from datetime import datetime

# Connection parameters
conexao = psycopg2.connect(
    database="projeto_museu",
    host="localhost",
    user="postgres",
    password="cesupa",
    port="5432"
)

# Print connection parameters
#print(conexao.get_dsn_parameters())

# Print connection status
#print(conexao.status)

# Função auxiliar para converter uma string em data ou retornar None se for 'NaN'
def parse_date(date_str):
    if isinstance(date_str, str) and date_str != 'NaN':
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None
    return None

# Create a cursor using a context manager
with conexao.cursor() as cursor:
    # CSV file path
    caminho_do_csv = r"C:\Users\hvell\Desktop\cesupa\banco_dados\projeto_museu\dados_tratados - occurrence.csv"

    # Read CSV into a DataFrame, skip header row
    df = pd.read_csv(caminho_do_csv, header=0)


    # Iterate over DataFrame rows and insert data into PostgreSQL
    for index, row in df.iterrows():
        
        decimal_latitude = float(row['decimalLatitude'].replace('.', '')) if not pd.isnull(row['decimalLatitude']) else None
        decimal_longitude = float(row['decimalLongitude'].replace('.', '')) if not pd.isnull(row['decimalLongitude']) else None
        repatriated = False if row['repatriated'] == 'NaN' else True if row['repatriated'] == 'True' else False 
        event_date = parse_date(row['eventDate'])        
        
        sql = "INSERT INTO occurrence (gbifID, accessRights,  license,  rightsHolder, institutionCode, collectionCode, basisOfRecord, occurrenceID, catalogNumber, occurrenceStatus, datasetKey, publishingCountry, lastInterpreted, issue, hasCoordinate, hasGeospatialIssues, protocol, lastParsed, lastCrawled, recordedBy, preparations, higherGeography, countryCode, stateProvince, locality, repatriated, county,eventDate, year, month, decimalLatitude, decimalLongitude, day, eventRemarks, typeStatus, infraspecificEpithet) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        dados = (row['gbifID'], row['accessRights'], row['license'], row['rightsHolder'], row['institutionCode'], row['collectionCode'], row['basisOfRecord'], row['occurrenceID'],row['catalogNumber'], row['occurrenceStatus'],
                 row['datasetKey'], row['publishingCountry'], row['lastInterpreted'], row['issue'], row['hasCoordinate'], row['hasGeospatialIssues'],row['protocol'], row['lastParsed'],row['lastCrawled'], row['recordedBy'],
                 row['preparations'], row['higherGeography'],row['countryCode'], row['stateProvince'], row['locality'], repatriated, row['county'], event_date, row['year'], row['month'], 
                 decimal_latitude, decimal_longitude, row['day'], row['eventRemarks'], row['typeStatus'], row['infraspecificEpithet'])

        try:
            cursor.execute(sql, dados)
            conexao.commit()
        except Exception as e:
            conexao.rollback()
            print(f"Erro na linha {index + 2}: {e}")


