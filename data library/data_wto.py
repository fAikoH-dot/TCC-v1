import requests
import pandas as pd
from datetime import datetime

def obter_dados_agricultura_wto(data_inicial, data_final):
    """
    Obtém dados de exportações de produtos agrícolas da API Time Series da OMC.

    Args:
        data_inicial (str): Data inicial no formato 'YYYY-MM'.
        data_final (str): Data final no formato 'YYYY-MM'.

    Returns:
        pandas.DataFrame: DataFrame com os dados de exportação de produtos agrícolas.
        Retorna None em caso de erro.
    """
    url_base = "https://data.wto.org/api/v1/public/TimeSeries/Data"
    # Codigos para exportações de produtos agrícolas. Esses codigos vem da documentação da API da WTO
    series_code = "AGRI_EXP"
    
    try:
        # Formata a url de acordo com a API
        url = f"{url_base}/{series_code}/?i=1&r=all&pc=all&ps={data_inicial}&pe={data_final}&freq=M"
        
        response = requests.get(url)
        response.raise_for_status()  # Verifica erros na requisição

        dados_json = response.json()

        # Extrai os dados relevantes
        dados = []
        for item in dados_json['Dataset']:
            for series in item['Series']:
                for obs in series['Obs']:
                    dados.append({
                        'Periodo': obs['Period'],
                        'Valor': obs['ObsValue']
                    })

        # Cria um DataFrame pandas
        df = pd.DataFrame(dados)

        # Converte a coluna 'Periodo' para datetime
        df['Periodo'] = pd.to_datetime(df['Periodo'], format='%Y-%m')

        return df

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição da API: {e}")
        return None
    except KeyError as e:
        print(f"Erro ao processar os dados da API: {e}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

# Definindo o período desejado
data_inicial = '2004-04'
data_final = '2025-11'

# Obtém os dados
df_agricultura = obter_dados_agricultura_wto(data_inicial, data_final)

# Imprime os dados ou salva em um arquivo CSV
if df_agricultura is not None:
    print(df_agricultura)
    # Exemplo de como salvar os dados em um arquivo CSV:
    # df_agricultura.to_csv("exportacoes_agricultura_wto.csv", index=False)