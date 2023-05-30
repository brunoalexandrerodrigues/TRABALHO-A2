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

def get_deputies_by_race(race):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
    params = {'itens': 100, 'pagina': 1}
    deputies = []

    while True:
        r = requests.get(url, params=params)
        data = r.json()['dados']
        
        for item in data:
            id_deputado = item['id']
            deputado = baixaDeputado(id_deputado)
            if 'dados' in deputado:
                ethnicity = deputado['dados']['ultimoStatus']['dados']['etnia']
                if ethnicity == race:
                    deputies.append(deputado['dados'])
        
        if r.json()['links'][0]['rel'] != 'next':
            break
        else:
            params['pagina'] += 1

    df = pd.DataFrame(deputies)
    return df

st.title('Lista de Deputados Pretos')

idLegislatura = st.slider('Escolha de qual legislatura você quer a lista de deputados', 50, 57, 57)

df = baixaDeputados(idLegislatura)
df_filtered = get_deputies_by_race('PRETA')

st.header('Lista de deputados pretos')
st.write(df_filtered)

st.header('Pautas de governo')
for index, linha in df_filtered.iterrows():
    with st.expander(linha['nome']):
        st.image(linha['urlFoto'], width=130)
        st.write('Nome: ' + linha['nome'])
        st.write('Partido: ' + linha['siglaPartido'])
        st.write('UF: ' + linha['siglaUf'])
        st.write('ID: ' + str(linha['id']))
        st.write('Email: ' + str(linha['email']))
        st.subheader('Pautas de governo:')
        pautas = linha['ultimoStatus']['pautas']
        if len(pautas) == 0:
            st.write('Nenhuma pauta de governo registrada.')
        else:
            for pauta in pautas:
                st.write('- ' + pauta)

if df_filtered.empty:
    st.subheader(':no_entry_sign: Nenhum deputado preto encontrado! :crying_cat_face:')

