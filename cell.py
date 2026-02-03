import io
import pandas as pd
import streamlit as st
from db import listar_itens_estoque

st.set_page_config(
    page_title="Estoque - Itens",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Listagem de Itens em Estoque")

df = listar_itens_estoque()

# Filtro por nome
filtro = st.text_input("🔍 Buscar item pelo nome")

if filtro:
    df = df[df["nome_item"].str.contains(filtro, case=False, na=False)]

# DataFrame para exibição
df_exibicao = df.rename(columns={
    "nome_item": "Nome do item",
    "grupo": "Grupo",
    "valor_item": "Valor do item",
    "quantidade_fisica": "Qtde Física"
})

# Tabela com formatação de moeda
st.dataframe(
    df_exibicao,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Valor do item": st.column_config.NumberColumn(
            "Valor do item",
            format="R$ %.2f"
        )
    }
)

# Métricas
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total de Itens",
    len(df)
)

col2.metric(
    "Quantidade Física Total",
    int(df["quantidade_fisica"].fillna(0).sum())
)

# Valor total do estoque (valor × quantidade)
valor_total_estoque = (
    df["valor_item"].fillna(0) *
    df["quantidade_fisica"].fillna(0)
).sum()

col3.metric(
    "Valor Total do Estoque",
    f"R$ {valor_total_estoque:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

# -------- EXPORTAÇÃO PARA EXCEL --------

def gerar_excel(df):
    output = io.BytesIO()

    df_export = df.rename(columns={
        "nome_item": "Nome do item",
        "grupo": "Grupo",
        "valor_item": "Valor do item",
        "quantidade_fisica": "Qtde Física"
    })

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_export.to_excel(writer, index=False, sheet_name="Estoque")

        workbook = writer.book
        worksheet = writer.sheets["Estoque"]

        formato_moeda = workbook.add_format({
            "num_format": "R$ #,##0.00"
        })

        worksheet.set_column("A:A", 40)
        worksheet.set_column("B:B", 25)
        worksheet.set_column("C:C", 15, formato_moeda)
        worksheet.set_column("D:D", 15)

    output.seek(0)
    return output

excel_file = gerar_excel(df)

st.download_button(
    label="📥 Exportar para Excel",
    data=excel_file,
    file_name="estoque_itens.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
