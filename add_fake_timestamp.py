"""
Script para adicionar coluna DtAtualizacao fake nas tabelas CDC que não têm essa coluna.

Uso:
    python add_fake_timestamp.py

Este script:
1. Lê os arquivos CDC em Parquet
2. Adiciona a coluna DtAtualizacao com timestamp atual nas tabelas que não têm
3. Salva o arquivo atualizado
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Configuração de quais tabelas precisam da coluna fake
TABLES_NEED_TIMESTAMP = {
    'produtos': True,
    'transacoes': False,  # Já tem DtCriacao
    'transacao_produto': True,
    'clientes': False  # Já tem DtAtualizacao
}

def add_fake_timestamp_to_cdc(cdc_path: Path) -> bool:
    """
    Adiciona coluna DtAtualizacao fake em um arquivo CDC se necessário.
    
    Args:
        cdc_path: Caminho do arquivo CDC em Parquet
        
    Returns:
        True se foi modificado, False caso contrário
    """
    # Extrai o nome da tabela do arquivo
    filename = cdc_path.name
    table_name = filename.split('_')[0]
    
    # Verifica se essa tabela precisa da coluna fake
    if table_name not in TABLES_NEED_TIMESTAMP or not TABLES_NEED_TIMESTAMP[table_name]:
        return False
    
    # Lê o arquivo
    df = pd.read_parquet(cdc_path)
    
    # Verifica se já tem a coluna
    if 'DtAtualizacao' in df.columns:
        return False
    
    # Adiciona a coluna com timestamp atual
    df['DtAtualizacao'] = datetime.now()
    
    # Salva o arquivo atualizado
    df.to_parquet(cdc_path, index=False, engine='pyarrow')
    
    return True


def main():
    """Processa todos os arquivos CDC no diretório data/cdc/"""
    cdc_dir = Path('data/cdc')
    
    if not cdc_dir.exists():
        print(f"❌ Diretório {cdc_dir} não encontrado")
        return
    
    print("=" * 70)
    print("ADICIONANDO COLUNA DtAtualizacao FAKE NOS ARQUIVOS CDC")
    print("=" * 70)
    
    # Lista todos os arquivos Parquet
    cdc_files = list(cdc_dir.glob('*.parquet'))
    
    if not cdc_files:
        print("⚠️  Nenhum arquivo CDC encontrado")
        return
    
    modified_count = 0
    skipped_count = 0
    
    for cdc_file in sorted(cdc_files):
        try:
            was_modified = add_fake_timestamp_to_cdc(cdc_file)
            
            if was_modified:
                print(f"✅ {cdc_file.name:50} | Coluna adicionada")
                modified_count += 1
            else:
                print(f"⏭️  {cdc_file.name:50} | Pulado")
                skipped_count += 1
                
        except Exception as e:
            print(f"❌ {cdc_file.name:50} | ERRO: {e}")
    
    print("=" * 70)
    print(f"📊 Resumo: {modified_count} modificados, {skipped_count} pulados")
    print("=" * 70)


if __name__ == "__main__":
    main()
