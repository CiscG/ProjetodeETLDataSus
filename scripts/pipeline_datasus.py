import os
import requests
import subprocess
from bs4 import BeautifulSoup

# Configurações para Rio Grande do Sul (RDRS...)
URL_BASE = "https://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/"
PASTA_RAW = os.path.expanduser("~/ETLProjetoDataSUS/data/raw")
PASTA_PROCESSED = os.path.expanduser("~/ETLProjetoDataSUS/data/processed")
BINARIO_BLAST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blast-dbf')

os.makedirs(PASTA_RAW, exist_ok=True)
os.makedirs(PASTA_PROCESSED, exist_ok=True)

def baixar_e_processar():
    print("Conectando ao DataSUS...")
    response = requests.get(URL_BASE)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Filtra apenas arquivos que começam com 'RDRS' (Rio Grande do Sul)
    arquivos = [link.get('href') for link in soup.find_all('a') 
                if link.get('href').endswith('.dbc') and link.get('href').startswith('RDRS')]
    
    print(f"Encontrados {len(arquivos)} arquivos do RS.")
    
    for arquivo in arquivos:
        caminho_raw = os.path.join(PASTA_RAW, arquivo)
        caminho_dbf = os.path.join(PASTA_PROCESSED, arquivo.replace('.dbc', '.dbf'))
        
        # Download
        if not os.path.exists(caminho_raw):
            print(f"Baixando: {arquivo}")
            r = requests.get(URL_BASE + arquivo)
            with open(caminho_raw, 'wb') as f:
                f.write(r.content)
        
        # Processamento
        if not os.path.exists(caminho_dbf):
            print(f"Convertendo: {arquivo}")
            subprocess.run([BINARIO_BLAST, caminho_raw, caminho_dbf], check=True)

if __name__ == "__main__":
    baixar_e_processar()
