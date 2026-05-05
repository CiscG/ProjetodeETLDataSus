import sys
import logging
from pyspark.sql import SparkSession

# Configuração de Logs para facilitar o debug no servidor
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DATASUS_CSV_Extraction")

def main():
    # Inicializa a sessão do Spark com suporte ao PostgreSQL
    spark = SparkSession.builder \
        .appName("DATASUS_Raw_CSV_Extraction") \
        .config("spark.jars", "/usr/share/java/postgresql.jar") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()

    try:
        logger.info("Iniciando leitura dos arquivos CSV do DATASUS...")
        
        # Caminho onde os CSVs brutos estão salvos no servidor
        csv_path = "/home/pessoal4/data/raw/datasus/*.csv"

        # LEITURA DO CSV: Configurações essenciais para dados do DATASUS
        raw_df = spark.read.csv(
            path=csv_path,
            header=True,
            sep=';',               # DATASUS geralmente usa ponto e vírgula
            encoding='ISO-8859-1', # Evita quebra de acentos (comum em dados do governo BR)
            inferSchema=True       # Tenta identificar inteiros e datas automaticamente
        )

        total_records = raw_df.count()
        logger.info(f"Leitura concluída. Total de registros encontrados: {total_records}")

        if total_records == 0:
            logger.warning("Nenhum dado encontrado nos arquivos CSV. Abortando carga.")
            sys.exit(0)

        logger.info("Iniciando a carga dos dados brutos no banco temporário...")

        # Escrita no Banco Temporário (PostgreSQL)
        # mode("overwrite") limpa a tabela antes de inserir os dados da nova extração
        raw_df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://localhost:5432/temp_db") \
            .option("dbtable", "raw_datasus_data") \
            .option("user", "pessoal4") \
            .option("password", "SUA_SENHA_AQUI") \
            .option("driver", "org.postgresql.Driver") \
            .mode("overwrite") \
            .save()

        logger.info("Carga no banco temporário concluída com sucesso!")

    except Exception as e:
        logger.error(f"Erro fatal durante a extração dos CSVs: {str(e)}")
        sys.exit(1)
    finally:
        spark.stop()
        logger.info("Sessão do Spark encerrada.")

if __name__ == "__main__":
    main()
