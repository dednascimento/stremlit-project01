import pandas as pd
import json as js
import streamlit as st

file = open('dados/vendas.json')
data = js.load(file)
df = pd.DataFrame.from_dict(data)

df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')
data = df['Data da Compra']
file.close()
