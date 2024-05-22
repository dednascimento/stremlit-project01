import streamlit as st
from dataset import df
from utils import *

# SIDEBAR
st.sidebar.title('Filtro')

with st.sidebar.expander('Categoria do Produto'):
    filtro_categoria = st.multiselect(
        'Categorias',
        df['Categoria do Produto'].unique(),
        df['Categoria do Produto'].unique(),
        help='Você pode selecionar um ou mais das categorias para análisar.',
        placeholder='Escolha uma categoria.'
    )

with st.sidebar.expander('Faixa de Preço'):
    filtro_preco = st.slider(
        'Preço',
        0, 5000,
        (0, 5000)
    )

with st.sidebar.expander('Data'):
    filtro_data = st.date_input(
        'Selecione a data',
        (df['Data da Compra'].min(),
            df['Data da Compra'].max()),
        help='Selecione a data das compras que deseja.',
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

# DATASET
st.title('Dataset de Vendas :bar_chart:')
with st.expander('Filtrar colunas'):
    colunas = st.multiselect(
        'Selecione as Colunas',
        list(df.columns),
        list(df.columns)
    )


filtro_dados = df.query(query)
filtro_dados = filtro_dados[colunas]

st.dataframe(filtro_dados)

st.markdown(
    f'''Esta tabela possui :blue[{filtro_dados.shape[0]}] linhas e
     :green[{filtro_dados.shape[1]}] colunas. Atualizado em :red[{(df['Data da Compra'].max()).year}].'''
)

st.markdown('Escreva o nome do arquivo.')
coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input(
        '',
        label_visibility='collapsed'
    )
    nome_arquivo += '.csv'
with coluna2:
    st.download_button(
        'Baixar arquivo csv',
        data=convert_csv(filtro_dados),
        file_name=nome_arquivo,
        mime='text/csv',
        on_click=mensagem_sucesso()
    )
