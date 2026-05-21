import sys
import logging
from pyspark.sql import SparkSession

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Spark_MySQL_Load")

def main():
    # Inicializa o Spark injetando o conector jar do MySQL
    spark = SparkSession.builder \
        .appName("DATASUS_Raw_To_MySQL") \
        .config("spark.jars", "/home/chico/ETLProjetoDataSUS/ProjetodeETLDataSus/jars/mysql-connector-j-8.0.33.jar") \
        .getOrCreate()

    try:
        logger.info("Iniciando leitura dos CSVs do DATASUS pelo Spark...")
        csv_path = "/home/chico/ETLProjetoDataSUS/ProjetodeETLDataSus/data/raw/datasus/*.csv"

        df = spark.read.csv(
            path=csv_path,
            header=True,
            sep=';',
            encoding='ISO-8859-1',
            inferSchema=True
        )

        total_registros = df.count()
        logger.info(f"Total de registros encontrados: {total_registros}. Enviando para o MySQL...")

        # String de conexão do MySQL local
        jdbc_url = "jdbc:mysql://localhost:3306/datasus_raw?allowPublicKeyRetrieval=true&useSSL=false"

        df.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", "raw_sim_data") \
            .option("user", "chico") \
            .option("password", "25356090!") \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .mode("overwrite") \
            .save()

        logger.info("Carga na tabela temporária/raw concluída com sucesso!")

    except Exception as e:
        logger.error(f"Erro durante o processamento do Spark: {str(e)}")
        sys.exit(1)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
