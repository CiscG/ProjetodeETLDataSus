import os
import requests
from bs4 import BeautifulSoup

# URL base do DataSUS (Exemplo: Dados de Internação - SIH)
# Você pode alterar a URL para outras bases do DataSUS
URL_BASE = "https://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/"
PASTA_DESTINO = os.path.expanduser("~/ETLProjetoDataSUS/data/raw")

# Cria a pasta caso não exista
os.makedirs(PASTA_DESTINO, exist_ok=True)

def baixar_arquivos():
    print(f"Conectando ao DataSUS em: {URL_BASE}")
    response = requests.get(URL_BASE)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Busca todos os links que terminam com .dbc
    arquivos = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.dbc')]
    
    print(f"Encontrados {len(arquivos)} arquivos. Iniciando download...")
    
    for arquivo in arquivos:
        url_arquivo = URL_BASE + arquivo
        caminho_local = os.path.join(PASTA_DESTINO, arquivo)
        
        if not os.path.exists(caminho_local):
            print(f"Baixando: {arquivo}...")
            with requests.get(url_arquivo, stream=True) as r:
                r.raise_for_status()
                with open(caminho_local, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"Concluído: {arquivo}")
        else:
            print(f"Já existe: {arquivo}, pulando...")

if __name__ == "__main__":
    baixar_arquivos()
