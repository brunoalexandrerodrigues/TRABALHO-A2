import streamlit as st
import requests

def get_deputies_data():
    url = "https://dadosabertos.camara.leg.br/api/v2/deputados?siglaUf=RJ&ordem=ASC&ordenarPor=nome"
    response = requests.get(url)
    data = response.json()
    deputies = data["dados"]
    return deputies

def get_deputy_ementas(deputy_id):
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputy_id}/proposicoes?ordem=ASC&ordenarPor=id"
    response = requests.get(url)
    data = response.json()
    ementas = []

    # Obtendo os autores das proposições
    autores_url = "https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json"
    autores_response = requests.get(autores_url)
    autores_data = autores_response.json()
    autores_dict = {proposicao["idProposicao"]: proposicao["nomeAutor"] for proposicao in autores_data["dados"]}

    # Obtendo os dados adicionais das ementas
    ementas_url = "https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json"
    ementas_response = requests.get(ementas_url)
    ementas_data = ementas_response.json()
    ementas_dict = {proposicao["id"]: proposicao for proposicao in ementas_data["dados"]}

    for proposicao in data["dados"]:
        ementa = proposicao["ementa"]
        id_proposicao = proposicao["id"]

        # Obtendo o autor da proposição
        autor = autores_dict.get(id_proposicao, "Autor Desconhecido")

        # Obtendo os dados adicionais da ementa
        ementa_detalhada = ementas_dict[id_proposicao].get("ementaDetalhada", "")
        keywords = ementas_dict[id_proposicao].get("keywords", "")

        ementas.append((ementa, autor, ementa_detalhada, keywords))

    return ementas

# Configurações da aplicação Streamlit
st.title("Dados dos Deputados do RJ")

deputies = get_deputies_data()

if deputies:
    selected_deputy = st.selectbox("Selecione o deputado", deputies, format_func=lambda deputy: deputy["nome"])
    deputy_id = selected_deputy["id"]
    ementas = get_deputy_ementas(deputy_id)

    st.subheader("Dados do Deputado")
    st.write("Nome:", selected_deputy["nome"])
    st.write("Partido:", selected_deputy["siglaPartido"])
    st.write("Ementas das Proposições:")
    for ementa, autor, ementa_detalhada, keywords in ementas:
        st.write("- Autor:", autor)
        st.write("  Ementa:", ementa)
        st.write("  Ementa Detalhada:", ementa_detalhada)
        st.write("  Palavras-chave:", keywords)
else:
    st.write("Não foram encontrados deputados do RJ.")
