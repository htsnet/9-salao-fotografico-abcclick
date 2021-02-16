import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# carrega os 2 dataframes
df_fotos = pd.read_csv('https://www.abcclick.com.br/streamlit/fotos.csv')
df_inscritos = pd.read_csv('https://www.abcclick.com.br/streamlit/inscritos.csv')

#remove as 2 linhas iniciais de controle do Orange
df_fotos = df_fotos[2:]
df_inscritos = df_inscritos[2:]
#converte lat e long em float
df_inscritos['latitude'] = pd.to_numeric(df_inscritos['latitude'], downcast="float")
df_inscritos['longitude'] = pd.to_numeric(df_inscritos['longitude'], downcast="float")
#cria campo de data
df_fotos['data'] = pd.to_datetime(df_fotos['Data da Inscrição']).dt.date
df_fotos['Concurso_Largura'] = pd.to_numeric(df_fotos['Concurso_Largura'])
df_fotos['Concurso_Altura'] = pd.to_numeric(df_fotos['Concurso_Altura'])

# Configuração inicial da página
st.set_page_config(page_title='9º Salão Nacional de Arte Fotográfica', page_icon='favicon.ico', layout='centered', )

def main():
      # definindo os parâmetros
    st.title('9º Salão Nacional de Arte Fotográfica')
    st.markdown("""
    Um retrato sobre um Concurso Fotográfico

    O **ABCclick Fotoclube** está promovendo seu 9º Salão Nacional de Arte Fotográfica (https://www.abcclick.com.br/9salao). 
    Conheça algumas curiosidades e informações sobre os participantes e fotos inscritas.

    Você pode ver na lateral esquerda os totais gerais.
    """)
    # informação na side bar
    st.sidebar.write("**Resumo**")
    st.sidebar.info('Total de Inscritos: {}'. format(df_inscritos.shape[0]))
    st.sidebar.info('Total de Fotos: {}'. format(df_fotos.shape[0]))

    # ativar se precisar ver os dados do dataframe
    if st.sidebar.checkbox('Ver dados de entrada'):
        st.header('Dados de entrada')
        st.write(df_fotos)
    # if st.sidebar.checkbox('Ver dados de entrada'):
    #     st.header('Dados de entrada')
    #     st.write(df_inscritos)

    st.subheader('Localização dos Inscritos')
    st.map(df_inscritos)

    st.subheader('Quantidade de fotos por dia')
    fig, ax = plt.subplots()
    g = sns.countplot(x='data', data=df_fotos)
    g.set_xticklabels(g.get_xticklabels(), rotation=90, fontsize=6)
    g.set(xlabel='Dia', ylabel='Qtde.')
    st.pyplot(fig)    

    st.subheader('Formato das fotos inscritas')
    fig, ax = plt.subplots()
    g = sns.countplot(x='Formato', data=df_fotos, order=reversed(df_fotos['Formato'].unique()))
    g.set_xticklabels(g.get_xticklabels(), rotation=90 )
    g.set(ylabel='Qtde.', xlabel='Formato')
    st.pyplot(fig)

    st.subheader('Resolução das fotos inscritas')
    sentido_foto = st.radio('Formato da foto', ('Paisagem', 'Retrato', 'Quadrada', 'Todas'))

    if sentido_foto == 'Paisagem':
        df_fotos_parcial = df_fotos[df_fotos['Formato'] == 'Paisagem']
    elif sentido_foto == 'Retrato':
        df_fotos_parcial = df_fotos[df_fotos['Formato'] == 'Retrato']
    elif sentido_foto == 'Quadrada':
        df_fotos_parcial = df_fotos[df_fotos['Formato'] == 'Quadrada']
    else:
        df_fotos_parcial = df_fotos.copy()

    sns.set_theme(color_codes=True)
    fig, ax = plt.subplots()
    g = sns.regplot(x='Concurso_Altura', y='Concurso_Largura', data=df_fotos_parcial,
     ax=ax, fit_reg=False, scatter_kws={'s':20, 'facecolor':'red'})
    #g = sns.relplot(x='Concurso_Altura', y='Concurso_Largura', data=df_fotos, ax=ax, scatter_kws={'s':20, 'facecolor':'red'})
    #g.set_xticklabels(g.get_xticklabels(), rotation=90 )
    g.set(ylabel='Largura', xlabel='Altura')
    st.pyplot(fig)

    st.subheader('Palavras mais usadas nos títulos')
    imagem_cloud_words = 'nuvemDePalavras.png'
    st.image(imagem_cloud_words)

if __name__ == '__main__':
	main()      