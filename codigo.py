pip install streamlit requests zipfile pandas
import streamlit as st
import requests
import zipfile
import pandas as pd

def baixaDeputados(idLegislatura):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura=' + str(idLegislatura)
    r = requests.get(url)
    deputados = r.json()['dados']
    df = pd.DataFrame(deputados)
    return df

def baixaProposicoesDeputado(idDeputado):
    url = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes?itens=100&autorId={idDeputado}&ordem=ASC&ordenarPor=id'
    r = requests.get(url)
    proposicoes = r.json()['dados']
    df = pd.DataFrame(proposicoes)
    return df

# Função para fazer o download do arquivo ZIP
def download_file(url, save_as):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(save_as, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

st.title('Lista de Deputados e Propostas de Governo')

idLegislatura = 57  # Defina aqui o valor da legislatura desejada

df = baixaDeputados(idLegislatura)

st.header('Lista de deputados do Rio de Janeiro')
df_rio_de_janeiro = df[df['siglaUf'] == 'RJ']  # Filtra apenas os deputados do Rio de Janeiro

selected_deputado = st.selectbox('Selecione um deputado:', df_rio_de_janeiro['nome'])

selected_deputado_info = df_rio_de_janeiro[df_rio_de_janeiro['nome'] == selected_deputado]

if not selected_deputado_info.empty:
    selected_deputado_info = selected_deputado_info.iloc[0]
    st.markdown('<h2 style="background-color: #ff9900; padding: 10px; border-radius: 5px; color: #ffffff;">Detalhes do Deputado</h2>', unsafe_allow_html=True)
    st.image(selected_deputado_info['urlFoto'], width=130)
    st.write('Nome: ' + selected_deputado_info['nome'])
    st.write('Partido: ' + selected_deputado_info['siglaPartido'])
    st.write('UF: ' + selected_deputado_info['siglaUf'])
    st.write('ID: ' + str(selected_deputado_info['id']))
    st.write('Email: ' + str(selected_deputado_info['email']))

    st.header('Propostas de Governo do Rio de Janeiro')

    # Definir URL do arquivo ZIP das propostas de governo do Rio de Janeiro
    url = 'https://cdn.tse.jus.br/estatistica/sead/odsele/proposta_governo/proposta_governo_2022_RJ.zip'
    zip_filename = 'proposta_governo_2022_RJ.zip'

    # Fazer o download do arquivo ZIP
    st.write('Baixando arquivo ZIP das propostas de governo...')
    download_file(url, zip_filename)
    st.write('Download concluído!')

    # Extrair o conteúdo do arquivo ZIP
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        st.write('Extraindo o arquivo ZIP das propostas de governo...')
        zip_ref.extractall('proposta_governo_2022_RJ')
        st.write('Extração concluída!')

    # Ler os dados do arquivo CSV extraído
    csv_filename = 'proposta_governo_2022_RJ/proposta_governo_2022_RJ.csv'
    df_propostas = pd.read_csv(csv_filename)

    # Filtrar as propostas de governo pelo ID do deputado selecionado
    df_propostas_deputado = df_propostas[df_propostas['id_cand'] == selected_deputado_info['id']]

    # Exibir os dados das propostas de governo
    st.dataframe(df_propostas_deputado)
else:
    st.write(':no_entry_sign: Sem informações disponíveis para o deputado selecionado!')

