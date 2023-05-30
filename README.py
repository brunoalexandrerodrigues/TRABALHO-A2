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

def get_deputies_by_state(state):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
    params = {'itens': 100, 'pagina': 1}
    deputies = []

    while True:
        r = requests.get(url, params=params)
        data = r.json()['dados']
        
        for item in data:
            id_deputado = item['id']
            deputado = baixaDeputado(id_deputado)
            if 'siglaUf' in deputado['ultimoStatus']['dados']:
                sigla_uf = deputado['ultimoStatus']['dados']['siglaUf']
                if sigla_uf == state:
                    deputies.append(deputado['ultimoStatus']['dados'])
        
        if r.json()['links'][0]['rel'] != 'next':
            break
        else:
            params['pagina'] += 1

    df = pd.DataFrame(deputies)
    return df

st.title('Lista de Parlamentares do Rio de Janeiro e suas Pautas de Governo')

idLegislatura = st.slider('Escolha de qual legislatura você quer a lista de deputados', 50, 57, 57)

df = baixaDeputados(idLegislatura)
df_rj = get_deputies_by_state('RJ')

st.header('Lista de parlamentares do Rio de Janeiro')
st.dataframe(df_rj[['nome', 'siglaPartido', 'siglaUf']])

st.header('Pautas de governo')
for index, row in df_rj.iterrows():
    deputado = baixaDeputado(row['id'])
    pautas = deputado['ultimoStatus']['dados']['pautas']
    if len(pautas) > 0:
        st.subheader(row['nome'])
        st.table(pd.DataFrame(pautas, columns=['Pauta de Governo']))
    else:
        st.subheader(row['nome'])
        st.write('Nenhuma pauta de governo registrada.')

if df_rj.empty:
    st.subheader(':no_entry_sign: Nenhum parlamentar encontrado para o Rio de Janeiro! :crying_cat_face:')




