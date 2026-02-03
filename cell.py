import fdb
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Estoque - Itens",
    page_icon="📦",
    layout="wide"
)

@st.cache_data(ttl=300)
def carregar_dados():
    conn = fdb.connect(
        host="matriz.aethos.cloud",
        database="/data/fbdatabases/4921_tnccellmobiledistribuidora3687_erp.fdb",
        user="CONVIDADO",
        password="w4!@x*+N",
        port=30183,
        charset="ISO8859_1"
    )

    query = """
        SELECT
            ip.ds_item   AS "Nome do item",
            ip.qt_fisico AS "Quantidade fisica"
        FROM item_principal ip
        ORDER BY ip.ds_item
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df

st.title("📦 Listagem de Itens em Estoque")

df = carregar_dados()

filtro = st.text_input("🔍 Buscar item pelo nome")

if filtro:
    df = df[df["Nome do item"].str.contains(filtro, case=False, na=False)]

st.dataframe(df, use_container_width=True, hide_index=True)

col1, col2 = st.columns(2)

col1.metric("Total de Itens", len(df))
col2.metric(
    "Quantidade Física Total",
    int(df["Quantidade fisica"].sum())
)
