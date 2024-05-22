import time
from dataset import df
import pandas as pd
import streamlit as st


def format_number(valor, prefix=''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefix} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefix} {valor:.2f} milhões'


# DF COM RECEITA POR ESTADO
df_rec_estado = df.groupby('Local da compra')[['Preço']].sum()
df_rec_estado = df[
    ['Local da compra', 'lat', 'lon']
].merge(
    # DF QUE VAMOS MESCLAR
    df_rec_estado,
    # COLUNA QUE VAMOS MESCLAR
    left_on='Local da compra',
    right_on='Local da compra',
    # SEGUIR O INDEX EXISTENTE
    right_index=True
).sort_values(
    'Preço',
    ascending=False
)

df_rec_estado = df_rec_estado.drop_duplicates('Local da compra')

# DF COM RECEITA MENSAL
df_rec_mensal = df.set_index('Data da Compra').groupby(
    pd.Grouper(freq='M')
)['Preço'].sum().reset_index()

df_rec_mensal['Ano'] = df_rec_mensal['Data da Compra'].dt.year
df_rec_mensal['Mes'] = df_rec_mensal['Data da Compra'].dt.month_name()

# DF COM RECEITA POR CATEGORIA
def_rec_categoria = df.groupby(
    'Categoria do Produto'
)[['Preço']].sum().sort_values('Preço', ascending=False)

# DF VENDEDORES
df_vendedores = pd.DataFrame(df.groupby('Vendedor')['Preço'].agg(['sum', 'count']))


@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')


def mensagem_sucesso():
    sucess = st.success('Arquiv foi baixado com sucesso.')
    time.sleep(3)
    sucess.empty()
