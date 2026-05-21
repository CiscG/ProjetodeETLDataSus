import os
import requests

def baixar_e_enviar(url, nome_arquivo):
    print(f"Tentando baixar: {nome_arquivo}...")
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status() # Lança erro se a URL não existir
        
        with open(nome_arquivo, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Verifica se o arquivo foi realmente criado e tem tamanho > 0
        if os.path.exists(nome_arquivo) and os.path.getsize(nome_arquivo) > 1000:
            print(f"Download concluído. Tamanho: {os.path.getsize(nome_arquivo)} bytes.")
            # Envio via SCP
            os.system(f"scp {nome_arquivo} chico@IP_DO_SEU_SERVIDOR:~/ETLProjetoDataSUS/data/raw/")
        else:
            print("Erro: O arquivo baixado parece estar vazio ou corrompido.")
            
    except Exception as e:
        print(f"Erro crítico durante o processo: {e}")

# Teste com uma URL real de um arquivo do RS
URL_TESTE = "https://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/RDRS2301.dbc"
baixar_e_enviar(URL_TESTE, "RDRS2301.dbc")
