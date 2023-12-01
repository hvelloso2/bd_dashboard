import pandas as pd
import psycopg2 

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

# Create a cursor using a context manager
with conexao.cursor() as cursor:
    # CSV file path
    caminho_do_csv = r"C:\Users\hvell\Desktop\cesupa\banco_dados\projeto_museu\dados_tratados - taxonomy.csv"

    # Read CSV into a DataFrame, skip header row
    df = pd.read_csv(caminho_do_csv, header=0)

    # Iterate over DataFrame rows and insert data into PostgreSQL
    for index, row in df.iterrows():
        sql = "INSERT INTO taxonomy (taxonKey, scientificName,  iucnRedListCategory,  specificEpithet, species) VALUES (%s,%s,%s,%s,%s)"
        dados = (row['taxonKey'], row['scientificName'], row['iucnRedListCategory'], row['specificEpithet'], row['species'])

        try:
            cursor.execute(sql, dados)
            conexao.commit()
        except Exception as e:
            conexao.rollback()
            print(f"Erro na linha {index + 2}: {e}")


