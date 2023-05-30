import streamlit as st
import pandas as pd
import requests

def baixaDeputados(idLegislatura):
    url = f'https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura={idLegislatura}'
    r = requests.get(url)
    deputados = r.json()['dados']
    df = pd.DataFrame(deputados)
    return df

def baixaDeputado(idDeputado):
    url = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{idDeputado}'
    r = requests.get(url)
    deputado = r.json()['dados']
    return deputado

def get_deputies_by_education(education):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
    params = {'itens': 100, 'pagina': 1}
    deputies = []

    while True:
        r = requests.get(url, params=params)
        data = r.json()['dados']
        
        for item in data:
            id_deputado = item['id']
            deputado = baixaDeputado(id_deputado)
            if 'escolaridade' in deputado['dados']:
                escolaridade = deputado['dados']['escolaridade']
                if escolaridade == education:
                    deputies.append(deputado['dados'])
        
        if r.json()['links'][0]['rel'] != 'next':
            break
        else:
            params['pagina'] += 1

    df = pd.DataFrame(deputies)
    return df

st.title('Lista de Parlamentares Formados em Comunicação')

idLegislatura = st.slider('Escolha de qual legislatura você quer a lista de deputados', 50, 57, 57)

df = baixaDeputados(idLegislatura)
df_communication = get_deputies_by_education('Comunicação')

st.header('Lista de parlamentares formados em Comunicação')
st.write(df_communication)




