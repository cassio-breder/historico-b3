#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importando biblioteca
import pandas as pd


# In[2]:


# Especificações das colunas

# DATA DO PREGÃO
# CODBDI - CÓDIGO BDI
# CODNEG - CÓDIGO DE NEGOCIAÇÃO DO PAPEL
# NOMRES - NOME RESUMIDO DA EMPRESA EMISSORA DO PAPEL
# PREABE - PREÇO DE ABERTURA DO PAPEL- MERCADO NO PREGÃO
# PREMAX - PREÇO MÁXIMO DO PAPEL- MERCADO NO PREGÃO
# PREMIN - PREÇO MÍNIMO DO PAPEL- MERCADO NO PREGÃO
# PREULT - PREÇO DO ÚLTIMO NEGÓCIO DO PAPEL-MERCADO NO PREGÃO
# QUATOT - QUANTIDADE TOTAL DE TÍTULOS NEGOCIADOS NESTE PAPEL- MERCADO
# VOLTOT - VOLUME TOTAL DE TÍTULOS NEGOCIADOS NESTE PAPEL- MERCADO

def read_files(path, name_file, year_date, type_file):   
    _file = f'{path}{name_file}{year_date}.{type_file}'

    colspecs = [(2, 10),
                (10, 12),
                (12, 24),
                (27, 39),
                (56, 69),
                (69, 82),
                (82, 95),
                (108, 121),
                (152, 170),
                (170, 188)]

    names = ['data_pregao', 'codbdi', 'sigla_acao', 'nome_acao',
             'preco_abertura', 'preco_maximo', 'preco_minimo',
             'preco_fechamento', 'qtd_negocios', 'volume_negocios']

    df = pd.read_fwf(_file, colspecs = colspecs, names = names, skiprows = 1)
    
    return df


# In[3]:


# Filtrar ações.
# TABELA DE CODBDI. 02 LOTE PADRÃO
def filter_stocks(df):
    df = df [df['codbdi'] == 2]
    df = df.drop(['codbdi'], 1)
    return df


# In[4]:


# Ajuste de data
def parse_date(df):
    df['data_pregao'] = pd.to_datetime(df['data_pregao'], format = '%Y%m%d')
    return df


# In[5]:


# Ajuste dos campos numéricos
def parse_values(df):
    df['preco_abertura'] = (df['preco_abertura'] / 100)
    df['preco_minimo'] = (df['preco_minimo'] / 100)
    df['preco_maximo'] = (df['preco_maximo'] / 100)
    df['preco_fechamento'] = (df['preco_fechamento'] / 100)
    df['qtd_negocios'] = (df['qtd_negocios']).astype(int)
    df['volume_negocios'] = (df['volume_negocios']).astype(int)
    return df


# In[6]:


# Juntando os arquivos
def concat_files(path, name_file, year_data, type_file, final_file):
    for i, y in enumerate(year_date):
        df = read_files(path, name_file, y, type_file)
        df = filter_stocks(df)
        df = parse_date(df)
        df = parse_values(df)
        
        if i == 0:
            df_final = df
        else:
            df_final = pd.concat([df_final, df])
            
    df_final.to_csv(f'{path}//{final_file}', index = False)


# In[7]:


# Arquivo final
year_date = ['2020', '2021', '2022']

path = f'/home/ac1/Documents/historico-b3/'

name_file = 'COTAHIST_A'

type_file = 'TXT'

final_file = 'final_file_bovespa.csv'

concat_files(path, name_file, year_date, type_file, final_file)

