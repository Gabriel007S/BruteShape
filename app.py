import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="BruteShape - Gestão de Treinos", layout="wide")
st.title("🏋️‍♂️ Gestão de Treinos - Academia BruteShape")

# ------------------- Funções para CSV -------------------
def read_csv(file_name, cols):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame(columns=cols)

def save_csv(df, file_name):
    df.to_csv(file_name, index=False)

# Arquivos CSV
alunos_file = "alunos.csv"
treinos_file = "treinos.csv"
evolucao_file = "evolucao.csv"

# Colunas de cada CSV
alunos_cols = ["Nome","Idade","Objetivo","DataInicio","Contato"]
treinos_cols = ["Aluno","Data","Exercicio","Series","Repeticoes","Carga","Observacoes"]
evolucao_cols = ["Aluno","Data","Peso","Braco","Peito","Cintura","Observacoes"]

# Carregar dados
alunos_df = read_csv(alunos_file, alunos_cols)
treinos_df = read_csv(treinos_file, treinos_cols)
evolucao_df = read_csv(evolucao_file, evolucao_cols)

# ------------------- Menu lateral -------------------
menu = st.sidebar.radio("Navegação", ["Cadastro de Alunos", "Treinos", "Evolução Física", "Relatórios", "Editar Contato"])

# ------------------- Cadastro de Alunos -------------------
if menu == "Cadastro de Alunos":
    st.header("Cadastro de Alunos")
    with st.form("form_aluno"):
        nome = st.text_input("Nome")
        idade = st.number_input("Idade", 10, 100)
        objetivo = st.text_input("Objetivo")
        data_inicio = st.date_input("Data de início")
        contato = st.text_input("Contato (WhatsApp/Email)")
        enviar = st.form_submit_button("Salvar")

    if enviar and nome:
        if nome in alunos_df["Nome"].values:
            st.warning("Aluno já cadastrado!")
        else:
            row = {"Nome": nome, "Idade": idade, "Objetivo": objetivo,
                   "DataInicio": str(data_inicio), "Contato": contato}
            alunos_df = pd.concat([alunos_df, pd.DataFrame([row])], ignore_index=True)
            save_csv(alunos_df, alunos_file)
            st.success(f"Aluno {nome} cadastrado!")

    st.dataframe(alunos_df)

# ------------------- Treinos -------------------
elif menu == "Treinos":
    st.header("Registro de Treinos")
    if alunos_df.empty:
        st.warning("Cadastre um aluno primeiro.")
    else:
        with st.form("form_treino"):
            aluno = st.selectbox("Aluno", alunos_df["Nome"])
            data = st.date_input("Data")
            exercicio = st.text_input("Exercício")
            series = st.number_input("Séries", 1, 20)
            repeticoes = st.number_input("Repetições", 1, 50)
            carga = st.number_input("Carga (kg)", 0, 500)
            obs = st.text_area("Observações")
            enviar = st.form_submit_button("Salvar")

        if enviar:
            row = {"Aluno": aluno, "Data": str(data), "Exercicio": exercicio,
                   "Series": series, "Repeticoes": repeticoes, "Carga": carga,
                   "Observacoes": obs}
            treinos_df = pd.concat([treinos_df, pd.DataFrame([row])], ignore_index=True)
            save_csv(treinos_df, treinos_file)
            st.success(f"Treino de {aluno} salvo!")

        st.dataframe(treinos_df)

# ------------------- Evolução Física -------------------
elif menu == "Evolução Física":
    st.header("Evolução Física")
    if alunos_df.empty:
        st.warning("Cadastre um aluno primeiro.")
    else:
        with st.form("form_evolucao"):
            aluno = st.selectbox("Aluno", alunos_df["Nome"])
            data = st.date_input("Data")
            peso = st.number_input("Peso (kg)", 0.0, 500.0, step=0.1)
            braco = st.number_input("Braço (cm)", 0.0, 80.0, step=0.1)
            peito = st.number_input("Peito (cm)", 0.0, 150.0, step=0.1)
            cintura = st.number_input("Cintura (cm)", 0.0, 150.0, step=0.1)
            obs = st.text_area("Observações")
            enviar = st.form_submit_button("Salvar")

        if enviar:
            row = {"Aluno": aluno, "Data": str(data), "Peso": peso, "Braco": braco,
                   "Peito": peito, "Cintura": cintura, "Observacoes": obs}
            evolucao_df = pd.concat([evolucao_df, pd.DataFrame([row])], ignore_index=True)
            save_csv(evolucao_df, evolucao_file)
            st.success(f"Evolução de {aluno} registrada!")

        st.dataframe(evolucao_df)

# ------------------- Relatórios -------------------
elif menu == "Relatórios":
    st.header("📊 Relatórios e Gráficos")
    if evolucao_df.empty:
        st.warning("Sem dados de evolução ainda.")
    else:
        aluno = st.selectbox("Selecione o aluno", alunos_df["Nome"].unique())
        df_aluno = evolucao_df[evolucao_df["Aluno"] == aluno]

        if not df_aluno.empty:
            st.subheader(f"Evolução de {aluno}")
            st.line_chart(df_aluno.set_index("Data")[["Peso", "Braco", "Peito", "Cintura"]])
        else:
            st.info("Nenhum dado de evolução para este aluno.")

# ------------------- Editar Contato -------------------
elif menu == "Editar Contato":
    st.header("Editar Contato do Aluno")
    
    if alunos_df.empty:
        st.warning("Nenhum aluno cadastrado.")
    else:
        aluno = st.selectbox("Selecione o aluno", alunos_df["Nome"])
        
        # Valor atual do contato
        contato_atual = alunos_df.loc[alunos_df["Nome"]==aluno, "Contato"].values[0]
        
        # Input para editar contato
        novo_contato = st.text_input("Contato", value=contato_atual)
        
        if st.button("Atualizar"):
            alunos_df.loc[alunos_df["Nome"]==aluno, "Contato"] = novo_contato
            save_csv(alunos_df, alunos_file)
            st.success(f"Contato de {aluno} atualizado!")
            st.dataframe(alunos_df)
