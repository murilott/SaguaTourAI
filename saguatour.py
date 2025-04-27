# iMPORTAR AS BIBLIOTECAS
import streamlit as st
import pandas as pd
import numpy as np
import os
from groq import Groq
#import plotly.express as px
import fitz

# python -m pip install -r req.txt
# python -m streamlit run bayes.py --server.port 8080

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

if not GROQ_API_KEY:
    st.error("A chave GROQ_API_KEY não foi definida corretamente!")
    st.stop()  
client = Groq(api_key=GROQ_API_KEY)

dataframes = {}

# função para extrair os arquivos     
def extract_files(uploader):
    text = ""
    for pdf in uploader:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc: 
            for page in doc:
                text += page.get_text("text") 
    return text

# def gerar_resposta(user_query):
#     prompt = f"Responda como um analista de dados. Pergunta: {user_query}"
#     response = client.chat.completions.create(model="llama3-8b-8192",
#                                               messages=[{"role": "user", "content": prompt}])
#     st.write("### Resposta do Agente:")
#     st.write(response.choices[0].message.content)
    
#     st.write("Resposta do Agente:")
#     st.write(response.choices[0].message.content)
    
#def gerar_grafico(graph_request, selected_file):
#    df = dataframes[selected_file]
#    if graph_request in df.columns:
#        fig = px.histogram(df, x=graph_request, title=f"Distribuição de {graph_request}")
#        st.plotly_chart(fig)
#    else:
#        st.warning("Coluna não encontrada no dataset!")

def chat_with_groq(prompt):
    context = "Você é um assistente virtual especializado em turismo local, com foco no bairro Saguaçu, em Joinville, Santa Catarina, Brasil. Seu papel é fornecer informações úteis, dicas personalizadas e sugestões de passeios, gastronomia, hospedagem, pontos turísticos, eventos locais e serviços no bairro e arredores. Seu tom deve ser acolhedor, informativo e entusiástico, como um guia local apaixonado pelo lugar."

    if st.session_state:
        context_file = st.session_state["document-text"]
    else:
        context_file = "Nenhum arquivo encontrado"
        
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"{context}"},
            {"role": "user", "content": f"{context_file}\n\n Pergunta: {prompt}"}
        ]
    )

    st.write("### Resposta do Agente:")
    st.write(response.choices[0].message.content)
    return response.choices[0].message.content

def consultar_dados(prompt):
    context = "Você é um assistente virtual especializado em turismo local, com foco no bairro Saguaçu, em Joinville, Santa Catarina, Brasil. Seu papel é fornecer informações úteis, dicas personalizadas e sugestões de passeios, gastronomia, hospedagem, pontos turísticos, eventos locais e serviços no bairro e arredores. Seu tom deve ser acolhedor, informativo e entusiástico, como um guia local apaixonado pelo lugar."

    if st.session_state:
        context_file = st.session_state["document-text"]
    else:
        context_file = "Nenhum arquivo encontrado"
        
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"{context}"},
            {"role": "user", "content": f"{context_file}\n\n Pergunta: {prompt}"}
        ]
    )

    st.write("### Resposta do Agente:")
    st.write(response.choices[0].message.content)
    return response.choices[0].message.content
    
# CRIAR A INTERFACE
def main():
    col1, col2, col3 = st.columns(3)
    col2.image("logo.png", width=200, caption="SaguaTour") 
    
    st.title("Turismo SaguaTour - Powered by AI")
    
    # Incluir uma imagem de acordo ao sistema escolhido
    with st.sidebar:
        st.header("Consulte dados sobre o Saguaçu!")
        st.write("Obtenha informações sobre o bairro Saguaçu")
        st.header("Upload Files")
        uploader = st.file_uploader("Adicione arquivos", type="pdf", accept_multiple_files=True)

    if uploader:
        text = extract_files(uploader)
        st.session_state["document-text"] = text

    # Query de pergunta
        
    user_input = st.text_input("Digite a sua pergunta")

    # Resultado pergunta
    
    if st.button("Enviar Pergunta") and user_input:
        chat_with_groq(user_input)

    # Query de gráfico
    
    #graph_request = st.text_input("Qual é a coluna que deseja ver o gráfico:")
    #selected_file = st.selectbox("Escolha um arquivo para visualizar:", list(dataframes.keys())) if dataframes else None

    # Resultado gráfico

    #if st.button("Gerar Gráfico") and graph_request and selected_file:
    #    gerar_grafico(graph_request, selected_file)

if __name__ == "__main__":
    main()
