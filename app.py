import streamlit as st
import plotly.express as px
from dataset import df
from utils import *
from graficos import *

st.set_page_config(layout='wide')
st.title('Dashboard de Vendas :shopping_trolley:')

# SIDEBAR FILTRO
st.sidebar.title('Filtros')
filtro_vendedor = st.sidebar.multiselect(
    'Vendedores',
    df['Vendedor'].unique(),
    help='Você pode selecionar um ou mais dos vendedores para análisar.',
    placeholder='Escolha um(a) vendedor(a).'
)

filtro_categoria = st.sidebar.multiselect(
    'Categorias',
    df['Categoria do Produto'].unique(),
    help='Você pode selecionar um ou mais das categorias para análisar.',
    placeholder='Escolha uma categoria.'
)

filtro_produto = st.sidebar.multiselect(
    'Produtos',
    df['Produto'].unique(),
    help='Você pode selecionar um ou mais dos produtos para análisar.',
    placeholder = 'Escolha um produto.'
)

# VENDEDOR
if filtro_vendedor and (not filtro_vendedor and not filtro_categoria):
    df = df[df['Vendedor'].isin(filtro_vendedor)]

elif filtro_vendedor and (filtro_produto and not filtro_categoria):
    df = df[(df['Vendedor'].isin(filtro_vendedor))]
    df = df[df['Produto'].isin(filtro_produto)]

# PRODUTO
elif filtro_produto and (not filtro_vendedor and not filtro_categoria):
    df = df[df['Produto'].isin(filtro_produto)]

# CATEGORIA
elif filtro_categoria and (not filtro_vendedor and not filtro_produto):
    df = df[df['Categoria do Produto'].isin(filtro_categoria)]

elif filtro_categoria and (filtro_vendedor and filtro_produto):
    df = df[(df['Vendedor'].isin(filtro_vendedor))]
    df = df[df['Produto'].isin(filtro_produto)]
    df = df[df['Categoria do Produto'].isin(filtro_categoria)]

elif filtro_categoria and filtro_vendedor:
    df = df[(df['Vendedor'].isin(filtro_vendedor))]
    df = df[df['Categoria do Produto'].isin(filtro_categoria)]

elif filtro_categoria and filtro_produto:
    df = df[df['Categoria do Produto'].isin(filtro_categoria)]
    df = df[df['Produto'].isin(filtro_produto)]

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