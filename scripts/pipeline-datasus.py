import pandas as pd
from sqlalchemy import create_engine
from simpledbf import Dbf5

# Conexão com MySQL (ajuste usuário/senha)
engine = create_engine('mysql+pymysql://usuario:senha@localhost/datasus_db')

def carregar_para_mysql(caminho_dbf):
    # Converte DBF para DataFrame Pandas
    dbf = Dbf5(caminho_dbf)
    df = dbf.to_dataframe()
    
    # Filtro: Município de Santa Rosa (Código IBGE 431720)
    # Nota: Verifique o nome real da coluna de município no seu arquivo (ex: 'MUNRES')
    df_filtrado = df[df['MUNRES'] == 431720]
    
    if not df_filtrado.empty:
        # Carrega para a tabela
        df_filtrado.to_sql('sih_santa_rosa', con=engine, if_exists='append', index=False)
        print(f"Dados de Santa Rosa inseridos com sucesso.")
    else:
        print("Nenhum dado encontrado para Santa Rosa neste arquivo.")
