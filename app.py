import streamlit as st
import plotly.express as px
from dataset import df
from utils import *
from graficos import *

st.set_page_config(layout='wide')
st.title('Dashboard de Vendas :shopping_trolley:')

# SIDEBAR FILTRO
st.sidebar.title('Filtro')

with st.sidebar.expander('Categoria do Produto'):
    filtro_categoria = st.multiselect(
        'Categorias',
        df['Categoria do Produto'].unique(),
        df['Categoria do Produto'].unique(),
        help='Você pode selecionar um ou mais das categorias para análisar.'
    )

with st.sidebar.expander('Faixa de Preço'):
    precoMax = int(df['Preço'].max())
    precoMin = int(df['Preço'].min())

    filtro_preco = st.slider(
        'Preço',
        precoMin, precoMax,
        (precoMin, precoMax)
    )

with st.sidebar.expander('Data'):
    filtro_data = st.date_input(
        'Selecione a data',
        (df['Data da Compra'].min(),
            df['Data da Compra'].max()),
        help='Selecione a data das compras que deseja.'
    )

with st.sidebar.expander('Vendedores'):
    filtro_vendedor = st.multiselect(
        'Vendedores',
        df['Vendedor'].unique(),
        df['Vendedor'].unique(),
        help='Você pode selecionar um ou mais dos vendedores para análisar.',
        placeholder='Escolha um(a) vendedor(a).'
    )

with st.sidebar.expander('Localidade'):
    filtro_local = st.multiselect(
        'Local da Compra',
        df['Local da compra'].unique(),
        df['Local da compra'].unique(),
        help='Você pode selecionar um ou mais regiões.',
        placeholder='Escolha um(a) vendedor(a).'
    )

# QUERY DE FILTRO:
query = '''
    `Categoria do Produto` in @filtro_categoria and \
    `Vendedor` in @filtro_vendedor and \
    `Local da compra` in @filtro_local and \
    @filtro_preco[0] <= Preço <= @filtro_preco[1] and \
    @filtro_data[0] <= `Data da Compra` <= @filtro_data[1]
'''

df = df.query(query)

# ABAS DASHBORD
aba1, aba2, aba3 = st.tabs(['Dataset', 'Receita', 'Vendedores'])

with aba1:
    st.dataframe(df)

with aba2:
    colum1, colum2 = st.columns(2)

    with colum1:
        st.metric('Receita Total:', format_number(df['Preço'].sum(), 'R$'))
        st.plotly_chart(grafico_rec_estado, use_container_width=True)
        st.plotly_chart(grafico_map_estado, use_container_width=True)

    with colum2:
        st.metric('Total de vendas:', format_number(df.shape[0]))
        st.plotly_chart(grafico_rec_mensal, use_container_width=True)
        st.plotly_chart(grafico_rec_categoria, use_container_width=True)

with aba3:
    colum1, colum2 = st.columns(2)

    with colum1:
        st.plotly_chart(grafico_rec_vendedor, use_container_width=True)
        st.dataframe(df_vendedores, use_container_width=True)

    with colum2:
        st.plotly_chart(grafico_vendedor_vendas, use_container_width=True)