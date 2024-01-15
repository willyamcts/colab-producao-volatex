import pandas as pd
import streamlit as st
import sqlite3
from datetime import datetime
from lib import Functions


st.set_page_config(
    layout="wide",
    page_title="Produção-Volatex"
)

# Verifica permissão
if st.session_state.get("tipo_usuario") != "admin" and st.session_state.get("tipo_usuario") != "operador":
    st.error("Você não tem permissão para acessar esta página.")
    st.stop()

# Variáveis Globais
conn = sqlite3.connect("db/db_producao.db")
c = conn.cursor()
db = Functions(conn)


##################### Sidebar #####################
st.sidebar.markdown("Desenvolvido por [Kanydian Esteves](https://www.linkedin.com/in/kanydian-esteves-07b0531a7/)")


##################### Funções #####################
def save(num_peca, peso, tear, operator, supplier, product, check):
    current_date = datetime.now()
    c.execute(
        "INSERT INTO production (num_peca, peso, tear, operator, supplier, product, check_production, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (num_peca, peso, tear, operator, supplier, product, check, current_date)
    )
    conn.commit()


##################### BODY #####################
st.title("Registro")
df_tear = db.get_tear()
tear = st.selectbox("Tear", df_tear["name"].unique())
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

df_product_supplier = db.get_products_supplier()
supplier    = col1.selectbox("Fornecedor", df_product_supplier["supplier"].unique())
supplier_filtered = df_product_supplier[df_product_supplier["supplier"] == supplier]
product     = col2.selectbox("Artigo", supplier_filtered["produto"].unique())
num_peca    = col3.text_input("Número da peça")
peso        = col4.number_input("Peso/KG")
df_operator = db.get_operator()
operator    = col5.selectbox("Operador", df_operator["name"].unique())
check       = st.text_input("Revisão")
insert      = st.button("Registrar")
if insert:
    save(num_peca, peso, tear, operator, supplier, product, check)
    st.success("Resgistrado com sucesso !!")


df_production          = db.get_production()
df_production_tear     = df_production[df_production["tear"] == tear]
df_production_supplier = df_production_tear[df_production_tear["supplier"] == supplier]
df_production_filtered = df_production_supplier[df_production_supplier["product"] == product]

st.markdown("## Último registro")
col1, col2 = st.columns(2)
col1.markdown(f"**Número da peça**: {df_production_filtered.iloc[-1]['num_peca']}")
col1.markdown(f"**Tear**:           {df_production_filtered.iloc[-1]['tear']}")
col1.markdown(f"**Fornecedor**:     {df_production_filtered.iloc[-1]['supplier']}")
col1.markdown(f"**Artigo**:         {df_production_filtered.iloc[-1]['product']}")
col2.markdown(f"**Peso**:           {df_production_filtered.iloc[-1]['peso']}")
col2.markdown(f"**Operador**:       {df_production_filtered.iloc[-1]['operator']}")
col2.markdown(f"**Revisão**:        {df_production_filtered.iloc[-1]['check_production']}")