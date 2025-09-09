import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="BruteShape - Gestão de Treinos", layout="wide")
//
st.title("🏋️‍♂️ Gestão de Treinos - Academia BruteShape")

# ----- Carregar dados se já existirem -----
if os.path.exists("alunos.csv"):
    st.session_state["alunos"] = pd.read_csv("alunos.csv")
else:
    st.session_state["alunos"] = pd.DataFrame(columns=["Nome", "Idade", "Objetivo", "Data_Inicio", "Contato"])

if os.path.exists("treinos.csv"):
    st.session_state["treinos"] = pd.read_csv("treinos.csv")
else:
    st.session_state["treinos"] = pd.DataFrame(columns=["Aluno", "Data", "Exercicio", "Series", "Repeticoes", "Carga", "Obs"])

if os.path.exists("evolucao.csv"):
    st.session_state["evolucao"] = pd.read_csv("evolucao.csv")
else:
    st.session_state["evolucao"] = pd.DataFrame(columns=["Aluno", "Data", "Peso", "Braco", "Peito", "Cintura", "Obs"])

# Menu lateral
menu = st.sidebar.radio("Navegação", ["Cadastro de Alunos", "Treinos", "Evolução Física", "Relatórios"])

# ----------------------- Cadastro de Alunos -----------------------
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
        st.session_state["alunos"].loc[len(st.session_state["alunos"])] = [nome, idade, objetivo, str(data_inicio), contato]
        st.session_state["alunos"].to_csv("alunos.csv", index=False)
        st.success(f"Aluno {nome} cadastrado!")

    st.dataframe(st.session_state["alunos"])

# ----------------------- Treinos -----------------------
elif menu == "Treinos":
    st.header("Registro de Treinos")
    if st.session_state["alunos"].empty:
        st.warning("Cadastre um aluno primeiro.")
    else:
        with st.form("form_treino"):
            aluno = st.selectbox("Aluno", st.session_state["alunos"]["Nome"])
            data = st.date_input("Data")
            exercicio = st.text_input("Exercício")
            series = st.number_input("Séries", 1, 20)
            repeticoes = st.number_input("Repetições", 1, 50)
            carga = st.number_input("Carga (kg)", 0, 500)
            obs = st.text_area("Observações")
            enviar = st.form_submit_button("Salvar")

        if enviar:
            st.session_state["treinos"].loc[len(st.session_state["treinos"])] = [aluno, str(data), exercicio, series, repeticoes, carga, obs]
            st.session_state["treinos"].to_csv("treinos.csv", index=False)
            st.success(f"Treino de {aluno} salvo!")

        st.dataframe(st.session_state["treinos"])

# ----------------------- Evolução Física -----------------------
elif menu == "Evolução Física":
    st.header("Evolução Física")
    if st.session_state["alunos"].empty:
        st.warning("Cadastre um aluno primeiro.")
    else:
        with st.form("form_evolucao"):
            aluno = st.selectbox("Aluno", st.session_state["alunos"]["Nome"])
            data = st.date_input("Data")
            peso = st.number_input("Peso (kg)", 0.0, 500.0, step=0.1)
            braco = st.number_input("Braço (cm)", 0.0, 80.0, step=0.1)
            peito = st.number_input("Peito (cm)", 0.0, 150.0, step=0.1)
            cintura = st.number_input("Cintura (cm)", 0.0, 150.0, step=0.1)
            obs = st.text_area("Observações")
            enviar = st.form_submit_button("Salvar")

        if enviar:
            st.session_state["evolucao"].loc[len(st.session_state["evolucao"])] = [aluno, str(data), peso, braco, peito, cintura, obs]
            st.session_state["evolucao"].to_csv("evolucao.csv", index=False)
            st.success(f"Evolução de {aluno} registrada!")

        st.dataframe(st.session_state["evolucao"])

# ----------------------- Relatórios -----------------------
elif menu == "Relatórios":
    st.header("📊 Relatórios e Gráficos")
    if st.session_state["evolucao"].empty:
        st.warning("Sem dados de evolução ainda.")
    else:
        aluno = st.selectbox("Selecione o aluno", st.session_state["alunos"]["Nome"].unique())
        df = st.session_state["evolucao"]
        df_aluno = df[df["Aluno"] == aluno]

        if not df_aluno.empty:
            st.subheader(f"Evolução de {aluno}")
            st.line_chart(df_aluno.set_index("Data")[["Peso", "Braco", "Peito", "Cintura"]])
        else:
            st.info("Nenhum dado de evolução para este aluno.")
