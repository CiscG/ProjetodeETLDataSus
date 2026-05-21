import subprocess
import os
import glob

# Configurações de diretórios
DIRETORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
BINARIO_BLAST = os.path.join(DIRETORIO_SCRIPT, 'blast-dbf')
PASTA_DADOS = os.path.join(DIRETORIO_SCRIPT, 'data') # Ajuste conforme necessário

def descomprimir_dbc(arquivo_dbc, arquivo_dbf):
    """Executa o binário blast-dbf para converter DBC em DBF."""
    try:
        subprocess.run([BINARIO_BLAST, arquivo_dbc, arquivo_dbf], check=True, capture_output=True)
        print(f"✓ Sucesso: {os.path.basename(arquivo_dbf)} gerado.")
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao descomprimir {arquivo_dbc}: {e.stderr.decode('utf-8')}")

def processar_pasta():
    """Busca arquivos .dbc na pasta e processa os que ainda não foram convertidos."""
    # Garante que o binário existe
    if not os.path.exists(BINARIO_BLAST):
        print(f"Erro: Binário não encontrado em {BINARIO_BLAST}")
        return

    # Busca todos os arquivos .dbc na pasta (ajuste o caminho se necessário)
    arquivos_dbc = glob.glob(os.path.join(DIRETORIO_SCRIPT, "*.dbc"))
    
    if not arquivos_dbc:
        print("Nenhum arquivo .dbc encontrado para processar.")
        return

    print(f"Encontrados {len(arquivos_dbc)} arquivos para processar...")

    for dbc in arquivos_dbc:
        dbf = dbc.replace('.dbc', '.dbf')
        
        # Só processa se o .dbf não existir (evita reprocessamento)
        if not os.path.exists(dbf):
            print(f"Processando: {os.path.basename(dbc)}...")
            descomprimir_dbc(dbc, dbf)
        else:
            print(f"Já processado: {os.path.basename(dbf)}")

if __name__ == "__main__":
    processar_pasta()
