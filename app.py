import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Tratamento de dados e definição de funções / variáveis
url = 'Customer-Churn-Records.csv'
dados = pd.read_csv(url)

# Criamos dicionários para traduzir termos em inglês presentes na base de dados

nomes_colunas = {
    'RowNumber'     : 'Linha',
    'CustomerId'    : "Id Cliente",
    'Surname'       : 'Sobrenome',
    'CreditScore'   : 'Score de Crédito',
    'Geography'     : 'País',
    'Gender'        : 'Gênero',
    'Age'           : 'Idade',
    'Tenure'        : 'Tempo de Relacionamento',
    'Balance'       : 'Saldo em Conta',
    'NumOfProducts' : 'Quantidade de Produtos',
    'HasCrCard'     : 'Cartão de Crédito',
    'IsActiveMember': 'Cliente Ativo',
    'EstimatedSalary': 'Salário Estimado',
    'Exited'        : 'Churn',
    'Complain'      : 'Reclamação',
    'Satisfaction Score': 'Nível de Satisfação',
    'Card Type'     : 'Tipo de Cartão',
    'Point Earned'  : 'Pontos do Cartão'
}

nomes_paises = {
    'France': 'França',
    'Spain' : 'Espanha',
    'Germany': 'Alemanha'
}

# Aplicamos os dicionários e substituímos as expressões
dados = dados.rename(columns = nomes_colunas)
dados['País'] = dados['País'].replace(nomes_paises)
dados['Gênero'] = dados['Gênero'].replace({'Female':'Feminino','Male':'Masculino'})

# Removemos as colunas que não são relevantes para a análise
dados = dados.drop(columns = ['Linha','Sobrenome','Id Cliente'])

# Calculamos a proporção (percentual) dos cancelamentos (Churn)
perc_churn = (dados['Churn'].sum() / len(dados))*100
perc_ativos = 100 - perc_churn

# Função para criar histogramas vinculando duas colunas
def histograma(coluna_1, coluna_2, dados):
    title = 'Clientes ' + coluna_2 + ' por ' + coluna_1
    x_label = coluna_1
    y_label = 'Quantidade'

    # Criar figura e eixos
    fig, ax = plt.subplots(figsize=(5, 3))

    # Criar o histograma
    sns.histplot(dados[dados[coluna_2] == 0][coluna_1], label='Ativos', kde=False, color='blue', ax=ax)
    sns.histplot(dados[dados[coluna_2] == 1][coluna_1], label='Cancelam', kde=False, color='red', ax=ax)

    # Configurar o gráfico
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()

    return fig


####################################################################################
########################## Criação da página #######################################
####################################################################################

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 200px !important;  /* Ajuste a largura conforme necessário */
            min-width: 200px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.header('Grupo 4 - Evolution Skills')
st.subheader('**Programa Evolution Skills: BB + FIAP**')

if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'Resultados'

def mudar_pagina(pagina):
    st.session_state['pagina'] = pagina

################### SIDEBAR ###################
st.sidebar.title("Menu")

if st.sidebar.button('Resultados'):
    mudar_pagina('Resultados')

if st.sidebar.button('Gráficos'):
    mudar_pagina('Gráficos')


########################### PÁGINA DE RESULTADOS #######################################

if st.session_state['pagina'] == 'Resultados':
    
    st.divider()
    # Gráfico de Pizza
    labels = 'Ativos', 'Clientes que cancelam'
    sizes = [perc_ativos, perc_churn]
    fig1, ax1 = plt.subplots(figsize=(4,4))
    ax1.pie(sizes,  autopct = '%1.1f%%', startangle = 90, textprops={'fontsize':14})
    ax1.legend(labels = labels, fontsize = 14, loc = 'upper left', bbox_to_anchor = (1,1))
    st.subheader('Percentual de Churn')
    st.pyplot(fig1)

    st.divider()
    # Apresentação do Perfil
    tab_r1,tab_r2,tab_r3 = st.tabs(['Perfil Churn','Por País','País / Idade'])

    with tab_r1:
        st.html('''
                <b>País:</b> Alemanha <br>
                <b>Gênero:</b> Feminino <br>
                <b>Idade:</b> Entre 32 e 45 anos
                ''')
                        
        perfil = dados[
                (dados['País'] == 'Alemanha') &
                (dados['Idade'] >= 32) &
                (dados['Idade'] <=45) &
                (dados['Gênero'] == 'Feminino')
               ]

        perc_churn = round(perfil['Churn'].sum() / perfil.shape[0] * 100, 2)
        perc_ativos = 100 - perc_churn

        sizes = [perc_ativos, perc_churn]
        fig1, ax1 = plt.subplots(figsize=(4,4))
        ax1.pie(sizes,  autopct = '%1.1f%%', startangle = 90, textprops={'fontsize':14})
        ax1.legend(labels = labels, fontsize = 14, loc = 'upper left', bbox_to_anchor = (1,1))
        st.subheader('Churn em clientes com o perfil identificado:')
        st.pyplot(fig1)
    
    with tab_r2:
        st.html('''
                <b>País:</b> Alemanha <br>
                ''')
                        
        perfil = dados[
                (dados['País'] == 'Alemanha') &
                (dados['Idade'] >= 32) &
                (dados['Idade'] <=45) &
                (dados['Gênero'] == 'Feminino')
               ]

        perc_churn = round(perfil['Churn'].sum() / perfil.shape[0] * 100, 2)
        perc_ativos = 100 - perc_churn

        sizes = [perc_ativos, perc_churn]
        fig1, ax1 = plt.subplots(figsize=(4,4))
        ax1.pie(sizes,  autopct = '%1.1f%%', startangle = 90, textprops={'fontsize':14})
        ax1.legend(labels = labels, fontsize = 14, loc = 'upper left', bbox_to_anchor = (1,1))
        st.subheader('Churn em clientes com o perfil identificado:')
        st.pyplot(fig1)
        

    with tab_r3:
        st.html('''
                <b>País:</b> Alemanha <br>
                <b>Idade:</b> 32 a 45 anos
                ''')
                        
        perfil = dados[
                (dados['País'] == 'Alemanha') &
                (dados['Idade'] >= 32) &
                (dados['Idade'] <=45)
               ]

        perc_churn = round(perfil['Churn'].sum() / perfil.shape[0] * 100, 2)
        perc_ativos = 100 - perc_churn

        sizes = [perc_ativos, perc_churn]
        fig1, ax1 = plt.subplots(figsize=(4,4))
        ax1.pie(sizes,  autopct = '%1.1f%%', startangle = 90, textprops={'fontsize':14})
        ax1.legend(labels = labels, fontsize = 14, loc = 'upper left', bbox_to_anchor = (1,1))
        st.subheader('Churn em clientes com o perfil identificado:')
        st.pyplot(fig1)


    ################## Apresentação do perfil engajado #########################

    st.divider()
    st.subheader('Relação entre Churn e Engajamento')

    engajados = dados[
        (dados['Quantidade de Produtos'] > 1) &
        (dados['Cartão de Crédito'] == 1) &
        (dados['Cliente Ativo'] == 1)
    ][['Quantidade de Produtos','Cartão de Crédito', 'Cliente Ativo', 'Pontos do Cartão', 'Churn']]

    texto1 = '''
            <b>Critérios para considerar cliente engajado:</b><br>
            <b>Cliente Ativo: </b> SIM <br>
            <b>Cartão de Crédito:</b> SIM<br>
            <b>Pontos do Cartão:</b> Mínimo 410 (Desconsiderado o quartil inferior)</br>
            <b>Quantidade de Produtos:</b> Mínimo 2<br>
            <b>Nível de Satisfação:</b> Mínimo de 4<br>
            <b>Público considerado engajado:</b> '''
    texto = texto1 + str(len(engajados))

    st.html(texto)

    nao_engajados = dados.drop(engajados.index)

    dados['Categoria'] = 'Não Engajado'
    dados.loc[engajados.index, 'Categoria'] = 'Engajado'

    resumo = dados.groupby(['Categoria', 'Churn']).size().reset_index(name='Total')
    resumo['Churn'] = resumo['Churn'].replace({1: 'Cancelado', 0: 'Não Cancelado'})
    dados['Categoria'] = 'Não Engajado'
    dados.loc[engajados.index, 'Categoria'] = 'Engajado'

    # Contar os registros por Categoria e Churn
    resumo = dados.groupby(['Categoria', 'Churn']).size().reset_index(name='Total')

    # Renomear os valores de Churn para facilitar a leitura
    resumo['Churn'] = resumo['Churn'].replace({1: 'Cancelado', 0: 'Não Cancelado'})

    # Calcular o percentual em relação ao total geral
    total_geral = resumo['Total'].sum()
    resumo['Percentual'] = (resumo['Total'] / total_geral) * 100

    # Adicionar linha de total
    linha_total = pd.DataFrame({
        'Categoria': ['Total'],
        'Churn': [''],
        'Total': [total_geral],
        'Percentual': [100.0]
    })

    # Filtrar os dados para cada categoria
    engajado_dados = resumo[resumo['Categoria'] == 'Engajado']
    nao_engajado_dados = resumo[resumo['Categoria'] == 'Não Engajado']

    # Criar os gráficos de pizza
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Definição das cores e rótulos
    cores_engajado = ['skyblue', 'red']
    cores_nao_engajado = ['lightgray', 'red']
    labels = ['Não Churn', 'Churn']

    # Gráfico para Engajados
    ax[0].pie(engajado_dados['Total'], textprops={'fontsize': 16}, autopct='%1.1f%%', colors=cores_engajado)
    ax[0].set_title('Engajados', fontsize=20)
    ax[0].legend(labels, loc="best", fontsize=16,  bbox_to_anchor = (1,1))  # Adicionando legenda

    # Gráfico para Não Engajados
    ax[1].pie(nao_engajado_dados['Total'], textprops={'fontsize':16}, autopct='%1.1f%%', colors=cores_nao_engajado)
    ax[1].set_title('Não Engajados', fontsize=20)
    ax[1].legend(labels, loc="best", fontsize=16,  bbox_to_anchor = (1,1))  # Adicionando legenda

    # Ajustar layout
    plt.tight_layout()

    # Exibir no Streamlit
    st.pyplot(fig)


####################### PÁGINA DE GRÁFICOS ##################################################

elif st.session_state['pagina'] == 'Gráficos':
    # Criar seleção de colunas
    colunas_y = sorted(['Score de Crédito', 'País', 'Gênero', 'Idade',
       'Tempo de Relacionamento', 'Saldo em Conta', 'Quantidade de Produtos',
       'Cartão de Crédito', 'Cliente Ativo', 'Salário Estimado', 
       'Reclamação', 'Nível de Satisfação', 'Tipo de Cartão',
       'Pontos do Cartão'])
    colunas_x = ['Churn', 'Cliente Ativo']
    
    col1, col2 = st.columns(2)

    with col1:
        coluna_1 = st.selectbox("Escolha o parâmetro a ser consultado:", colunas_y)
    with col2:
        coluna_2 = st.selectbox("Escolha a variável categórica:", colunas_x)

    # Botão para gerar o gráfico
    if st.button("Gerar Histograma"):
        fig = histograma(coluna_1, coluna_2, dados)
        st.pyplot(fig)  # Exibir gráfico no Streamlit
