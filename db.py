import fdb
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def listar_itens_estoque():
    conn = fdb.connect(
        host="matriz.aethos.cloud",
        database="/data/fbdatabases/4921_tnccellmobiledistribuidora3687_erp.fdb",
        user="CONVIDADO",
        password="w4!@x*+N",
        port=30183,
        charset="ISO8859_1"
    )

    query = """
        select
            ip.ds_item as "nome_item",
            sub.ds_subnivel as "grupo",
            i.VL_VENDAITEM as "valor_item",
            ip.qt_fisico as "quantidade_fisica"
        from item_principal ip
        join subnivel sub on (ip.id_subnivel = sub.id_subnivel)
        join item i on (ip.id_item = i.id_item)
        ORDER BY ip.ds_item
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df
