
import os
from ftplib import FTP
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FTP_DATASUS")

def main():
    dest_dir = "/home/chico/ETLProjetoDataSUS/ProjetodeETLDataSus/data/raw/datasus/"
    os.makedirs(dest_dir, exist_ok=True)

    logger.info("Conectando ao FTP do DATASUS...")
    try:
        ftp = FTP('ftp.datasus.gov.br')
        ftp.login()

        # Acessando a pasta de Mortalidade (SIM) como exemplo
        ftp.cwd('dissemin/publicos/SIM/CID10/DORES/')

        # Pega os últimos 2 arquivos CSV listados
        files = [f for f in ftp.nlst() if f.endswith('.csv') or f.endswith('.CSV')][-2:]

        for filename in files:
            local_filepath = os.path.join(dest_dir, filename)
            logger.info(f"Baixando arquivo: {filename}")
            with open(local_filepath, 'wb') as local_file:
                ftp.retrbinary(f"RETR {filename}", local_file.write)

        ftp.quit()
        logger.info("Todos os downloads foram concluídos com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao conectar ou baixar do FTP: {str(e)}")

if __name__ == "__main__":
    main()
