import os
from ftplib import FTP
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # Destino no seu Ubuntu Server
    dest_dir = "/home/chico/ETLProjetoDataSUS/ProjetodeETLDataSus/data/raw/datasus/"
    os.makedirs(dest_dir, exist_ok=True)

    logging.info("Conectando ao FTP do DATASUS...")
    ftp = FTP('ftp.datasus.gov.br')
    ftp.login()

    # Navegando até a pasta de dados de Mortalidade (SIM) - Exemplo: CID10
    ftp.cwd('dissemin/publicos/SIM/CID10/DORES/')

    # Lista os arquivos disponíveis e pega os 2 mais recentes como exemplo (arquivos .csv)
    files = [f for f in ftp.nlst() if f.endswith('.csv')][-2:]

    for filename in files:
        local_filepath = os.path.join(dest_dir, filename)
        logging.info(f"Baixando {filename}...")
        with open(local_filepath, 'wb') as local_file:
            ftp.retrbinary(f"RETR {filename}", local_file.write)

    ftp.quit()
    logging.info("Download concluído com sucesso.")

if __name__ == "__main__":
    main()
