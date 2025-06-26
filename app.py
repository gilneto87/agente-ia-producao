import streamlit as st
import pandas as pd
import pdfplumber
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análise de Produção e Qualidade", layout="wide")

st.title("📊 Agente IA - Análise de Produção, Qualidade e Planos de Ação")

uploaded_file = st.file_uploader("📁 Faça upload de um arquivo Excel (.xlsx) ou PDF com tabelas", type=["xlsx", "pdf"])

def read_excel(file):
    return pd.read_excel(file)

def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"
    return all_text

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "xlsx":
        df = read_excel(uploaded_file)
        st.success("✅ Planilha carregada com sucesso!")
        st.dataframe(df)

        if "Indicador" in df.columns and "Valor" in df.columns:
            fig, ax = plt.subplots()
            df.groupby("Indicador")["Valor"].sum().plot(kind="bar", ax=ax)
            ax.set_title("Indicadores - Total por Tipo")
            st.pyplot(fig)

    elif file_type == "pdf":
        text = read_pdf(uploaded_file)
        st.success("✅ PDF carregado com sucesso!")
        st.text_area("Conteúdo extraído do PDF:", text, height=300)

    else:
        st.error("❌ Tipo de arquivo não suportado.")
