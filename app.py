import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="BruteShape - Gestão de Treinos", layout="wide")
st.title("🏋️‍♂️ Gestão de Treinos - Academia BruteShape")

# ----- Conectar com Google Sheets -----
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("BruteShape")  # Nome da planilha

# Função para ler aba
def read_sheet(tab_name):
    try:
        worksheet = sheet.worksheet(tab_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

# Função para escrever na aba
def append_sheet(tab_name, row):
    worksheet = sheet.worksheet(tab_name)
    worksheet.append_row(row)

# ----- Carregar dados -----
alunos_df = read_sheet("Alunos")
treinos_df = read_sheet("Treinos")
evolucao_df = read_sheet("Evolucao")

# Menu lateral
menu = st.sidebar.radio("Navegação", ["Cadastro de Alunos", "Treinos", "Evolução Física", "Relatórios", "Editar Alunos"])

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
        row = [nome, idade, objetivo, str(data_inicio), contato]
        append_sheet("Alunos", row)
        st.success(f"Aluno {nome} cadastrado!")
        alunos_df = read_sheet("Alunos")

    st.dataframe(alunos_df)

# ----------------------- Treinos -----------------------
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
            row = [aluno, str(data), exercicio, series, repeticoes, carga, obs]
            append_sheet("Treinos", row)
            st.success(f"Treino de {aluno} salvo!")
            treinos_df = read_sheet("Treinos")

        st.dataframe(treinos_df)

# ----------------------- Evolução Física -----------------------
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
            row = [aluno, str(data), peso, braco, peito, cintura, obs]
            append_sheet("Evolucao", row)
            st.success(f"Evolução de {aluno} registrada!")
            evolucao_df = read_sheet("Evolucao")

        st.dataframe(evolucao_df)

# ----------------------- Relatórios -----------------------
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

# ----------------------- Editar Alunos -----------------------
elif menu == "Editar Alunos":
    st.header("Editar Informações do Aluno")
    
    if alunos_df.empty:
        st.warning("Nenhum aluno cadastrado.")
    else:
        aluno = st.selectbox("Selecione o aluno", alunos_df["Nome"])
        
        # Pegar valores atuais
        idade_atual = alunos_df.loc[alunos_df["Nome"]==aluno, "Idade"].values[0]
        objetivo_atual = alunos_df.loc[alunos_df["Nome"]==aluno, "Objetivo"].values[0]
        contato_atual = alunos_df.loc[alunos_df["Nome"]==aluno, "Contato"].values[0]
        
        # Inputs para editar
        novo_idade = st.number_input("Idade", value=int(idade_atual))
        novo_objetivo = st.text_input("Objetivo", value=objetivo_atual)
        novo_contato = st.text_input("Contato", value=contato_atual)
        
        if st.button("Atualizar"):
            worksheet = sheet.worksheet("Alunos")
            cell = worksheet.find(aluno)
            row_number = cell.row
            
            worksheet.update_cell(row_number, alunos_df.columns.get_loc("Idade")+1, novo_idade)
            worksheet.update_cell(row_number, alunos_df.columns.get_loc("Objetivo")+1, novo_objetivo)
            worksheet.update_cell(row_number, alunos_df.columns.get_loc("Contato")+1, novo_contato)
            
            st.success(f"Dados de {aluno} atualizados!")
            
            # Recarregar tabela
            alunos_df = read_sheet("Alunos")
            st.dataframe(alunos_df)
