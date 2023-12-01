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

# Print connection status
print(conexao.status)

# Create a cursor using a context manager
with conexao.cursor() as cursor:
    # CSV file path
    caminho_do_csv = r"C:\Users\hvell\Desktop\cesupa\banco_dados\projeto_museu\dados_tratados - kingdom.csv"

    # Read CSV into a DataFrame, skip header row
    df = pd.read_csv(caminho_do_csv, header=0)

    # Iterate over DataFrame rows and insert data into PostgreSQL
    for index, row in df.iterrows():
        # Insert into tabela1
        sql_tabela1 = "INSERT INTO tabela1 (coluna1, coluna2) VALUES (%s, %s)"
        dados_tabela1 = (row['coluna1_tabela1'], row['coluna2_tabela1'])

        # Insert into tabela2
        sql_tabela2 = "INSERT INTO tabela2 (taxonokey, scientificName, coluna3) VALUES (%s, %s, %s)"
        dados_tabela2 = (row['coluna1_tabela2'], row['coluna2_tabela2'], row['coluna3_tabela2'])

        try:
            # Execute for tabela1
            cursor.execute(sql_tabela1, dados_tabela1)
            
            # Execute for tabela2
            cursor.execute(sql_tabela2, dados_tabela2)

            # Commit changes
            conexao.commit()
        except Exception as e:
            # Rollback in case of an error
            conexao.rollback()
            print(f"Erro na linha {index + 2}: {e}")
