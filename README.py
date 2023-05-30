import streamlit as st
import pandas as pd
import requests

def baixaDeputados(idLegislatura):
    url = f'https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura={idLegislatura}'
    r = requests.get(url)
    deputados = r.json()['dados']
    df = pd.DataFrame(deputados)
    return df

def filter_candidates(df):
    df_filtered = df[(df['corRaca'] == 'PRETA') & (df['sexo'] != 'MASCULINO')]
    return df_filtered

st.title('Lista de Deputados Pretos')

idLegislatura = st.slider('Escolha de qual legislatura você quer a lista de deputados', 50, 57, 57)

df = baixaDeputados(idLegislatura)
df_filtered = filter_candidates(df)

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
