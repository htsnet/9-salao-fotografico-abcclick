import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# LOG
import logging
LOGS_FORMAT = "%(levelname)s %(asctime)s.%(msecs)03d -%(message)s"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOGS_FORMAT)
file_handler = logging.FileHandler('activity.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# carrega os 2 dataframes
df_fotos = pd.read_csv('fotos.csv')
df_inscritos = pd.read_csv('inscritos.csv')

#converte lat e long em float
df_inscritos['latitude'] = pd.to_numeric(df_inscritos['latitude'], downcast="float")
df_inscritos['longitude'] = pd.to_numeric(df_inscritos['longitude'], downcast="float")
#cria campo de data
df_fotos['data'] = pd.to_datetime(df_fotos['Data da Inscrição']).dt.date
df_fotos['Concurso_Largura'] = pd.to_numeric(df_fotos['Concurso_Largura'])
df_fotos['Concurso_Altura'] = pd.to_numeric(df_fotos['Concurso_Altura'])

# Configuração inicial da página
st.set_page_config(page_title='9º Salão Nacional de Arte Fotográfica', page_icon='favicon.ico', layout='centered', )


#para esconder o menu do próprio streamlit 
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""

def main():
    logger.info("Acesso ao site")
    # definindo os parâmetros
    st.title('9º Salão Nacional de Arte Fotográfica')
    st.markdown("""
    Um retrato sobre um Concurso Fotográfico

    O **ABCclick Fotoclube** está promovendo seu 9º Salão Nacional de Arte Fotográfica (https://www.abcclick.com.br/9salao). 
    Conheça algumas curiosidades e informações sobre os participantes e fotos inscritas.

    Veja esta **[publicação no LinkedIn](https://www.linkedin.com/posts/hamiltontenoriodasilva_vejam-um-pequeno-retrato-sobre-participantes-activity-6767073669417054208-7Rd2)** com comentários sobre o assunto.

    Você pode ver na lateral esquerda os totais gerais.
    """)

    #esconde menu do streamlit da direita
    #precisa ter a variável criada
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    # informação na side bar
    logo = 's9-vers.jpg'
    st.sidebar.image(logo)
    
    st.sidebar.write("**Resumo**")
    st.sidebar.info('Total de Inscritos: {}'. format(df_inscritos.shape[0]))
    st.sidebar.info('Total de Fotos: {}'. format(df_fotos.shape[0]))


    # ativar se precisar ver os dados do dataframe
    # if st.sidebar.checkbox('Ver dados de entrada'):
    #     st.header('Dados de entrada')
    #     st.write(df_fotos)
    # if st.sidebar.checkbox('Ver dados de entrada'):
    #     st.header('Dados de entrada')
    #     st.write(df_inscritos)

    st.subheader('Localização dos Inscritos')
    #prepara 2 colunas
    col1, col2 = st.beta_columns((1,6))
    todos_estados = df_inscritos.Estado.unique().tolist()
    todos_estados.sort()
    estados = ['Todos']
    for i in todos_estados:
        estados.append(i)
    estado = col1.radio('Estado', (estados), index=0 )
    if estado == 'Todos':
        df_incritos_estado = df_inscritos.copy()
    else:
        df_incritos_estado = df_inscritos[df_inscritos['Estado'] == estado]
    col2.map(df_incritos_estado)

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
    col3, col4 = st.beta_columns((1,6))
    todos_formatos = df_fotos.Formato.unique().tolist()
    formatos = ['Todas']
    for i in todos_formatos:
        formatos.append(i)
    sentido_foto = col3.radio('Formato da foto', (formatos), index=0 )

    if sentido_foto == 'Todas':
        df_fotos_parcial = df_fotos.copy()
    else:
        df_fotos_parcial = df_fotos[df_fotos['Formato'] == sentido_foto]

    sns.set_theme(color_codes=True)
    fig, ax = plt.subplots()
    g = sns.regplot(x='Concurso_Largura', y='Concurso_Altura', data=df_fotos_parcial,
     ax=ax, fit_reg=False, scatter_kws={'s':20, 'facecolor':'red'})
    #g = sns.relplot(x='Concurso_Altura', y='Concurso_Largura', data=df_fotos, ax=ax, scatter_kws={'s':20, 'facecolor':'red'})
    #g.set_xticklabels(g.get_xticklabels(), rotation=90 )
    g.set(ylabel='Altura', xlabel='Largura')
    col4.pyplot(fig)

    st.subheader('Palavras mais usadas nos títulos')
    imagem_cloud_words = 'nuvemDePalavras.png'
    st.image(imagem_cloud_words)

if __name__ == '__main__':
	main()      