
import pandas as pd
import os

def convert_csv_to_parquet(csv_path, parquet_path):
    """
    Converte um arquivo CSV para o formato Parquet.

    Args:
        csv_path (str): O caminho para o arquivo CSV de entrada.
        parquet_path (str): O caminho para o arquivo Parquet de saída.
    """
    try:
        df = pd.read_csv(csv_path, sep=';', encoding='MacRoman')
        df.to_parquet(parquet_path, index=False)
        print(f"Arquivo '{csv_path}' convertido para '{parquet_path}' com sucesso.")
    except FileNotFoundError:
        print(f"Erro: O arquivo '{csv_path}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao converter '{csv_path}': {e}")

if __name__ == "__main__":
    data_dir = "data"
    
    files_to_convert = [
        "Base_de_Transacoes_Cupons_Capturados.csv",
        "Base_Simulada_Pedestres_Av_Paulista.csv",
        "Base_Cadastral_de_Players.csv",
        "Base_de_Teste_com_Lojas_e_Valores.csv"
    ]
    
    for file_name in files_to_convert:
        csv_path = os.path.join(data_dir, file_name)
        parquet_path = os.path.join(data_dir, file_name.replace(".csv", ".parquet"))
        convert_csv_to_parquet(csv_path, parquet_path)
