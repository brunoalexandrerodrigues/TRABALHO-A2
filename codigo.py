import streamlit as st
import pandas as pd
import requests

# Definir estilo da página
st.markdown(
    """
    <style>
    .reportview-container {
        background: url('https://www.rio.rj.gov.br/igstatic/50/13/00/5013008.jpg');
        background-size: cover;
    }
    .title {
        color: #ffffff;
    }
    .highlight {
        background-color: #ff9900;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def baixaDeputados(idLegislatura):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura=' + str(idLegislatura)
    r = requests.get(url)
    deputados = r.json()['dados']
    df = pd.DataFrame(deputados)
    return df

def baixaPropostasDeputado(idDeputado):
    url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?itens=100&idAutor=' + str(idDeputado)
    r = requests.get(url)
    propostas = r.json()['dados']
    df = pd.DataFrame(propostas)
    return df

# Título com estilo
st.markdown("<h1 style='text-align: center;'>Lista de Deputados do Rio de Janeiro</h1>", unsafe_allow_html=True)

idLegislatura = 57  # Considerando a legislatura atual
df_deputados = baixaDeputados(idLegislatura)

# Filtra a lista apenas para o estado do Rio de Janeiro
df_rio_de_janeiro = df_deputados[df_deputados['siglaUf'] == 'RJ']

# Exibe a lista de deputados do Rio de Janeiro com nome e ID
st.header('Lista de Deputados do Rio de Janeiro')
df_display = df_rio_de_janeiro[['nome', 'id']]
selected_row = st.radio('Selecione um deputado:', df_display['nome'], index=0)
selected_deputado = df_display[df_display['nome'] == selected_row]

# Obtém as informações detalhadas do deputado selecionado
deputado_id = selected_deputado['id'].values[0]
selected_deputado_info = df_rio_de_janeiro[df_rio_de_janeiro['id'] == deputado_id]

# Exibe detalhes adicionais do deputado selecionado com destaque
if not selected_deputado_info.empty:
    selected_deputado_info = selected_deputado_info.iloc[0]
    st.header('Detalhes do Deputado')
    st.markdown('<div class="highlight"><h3>{}</h3></div>'.format(selected_deputado_info['nome']), unsafe_allow_html=True)
    st.subheader('Foto:')
    st.image(selected_deputado_info['urlFoto'], width=200)
    st.subheader('Informações Pessoais:')
    st.write('ID: ' + str(selected_deputado_info['id']))
    st.write('Email: ' + str(selected_deputado_info['email']))
    st.write('Rede Social: ' + str(selected_deputado_info['redeSocial']))
    st.write('Data de Nascimento: ' + str(selected_deputado_info['dataNascimento']))
    st.write('Escolaridade: ' + str(selected_deputado_info['escolaridade']))
    st.write('Rede Social: ' + str(selected_deputado_info['redeSocial']))


