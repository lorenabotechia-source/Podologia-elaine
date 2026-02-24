import streamlit as st
import sqlite3
import pandas as pd

# --- CONFIGURAÇÃO VISUAL (AZUL, BRANCO, VERDE) ---
st.set_page_config(page_title="Ficha Podológica - Elaine Souza", layout="wide")

st.markdown("""
    <style>
    /* Cor de fundo da página */
    .stApp { background-color: #FFFFFF; }
    
    /* Estilo dos Títulos (Azul) */
    h1, h2, h3, h4 { color: #1E3A8A !important; font-family: 'Arial'; }
    
    /* Estilo dos Botões (Verde) */
    .stButton>button {
        background-color: #10B981 !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        height: 3em;
        width: 100%;
    }
    
    /* Ajuste de bordas dos campos (Azul) */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-color: #1E3A8A !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DO BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect('podologia_elaine.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, data_nasc TEXT, endereco TEXT, telefone TEXT,
            bairro TEXT, cidade TEXT, cep TEXT, profissao TEXT,
            trabalha TEXT, esporte TEXT, calcado TEXT, cirurgia TEXT,
            medicamentos TEXT, medicamentos_quais TEXT,
            curativo1 TEXT, curativo2 TEXT, curativo3 TEXT, curativo4 TEXT, curativo5 TEXT,
            granuloma TEXT, ortese TEXT, artelho TEXT, inicio TEXT, final TEXT,
            condicoes TEXT, ass_paciente TEXT, profissional TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_dados(dados):
    conn = sqlite3.connect('podologia_elaine.db')
    c = conn.cursor()
    colunas = ', '.join(dados.keys())
    placeholders = ', '.join(['?'] * len(dados))
    c.execute(f"INSERT INTO pacientes ({colunas}) VALUES ({placeholders})", list(dados.values()))
    conn.commit()
    conn.close()

init_db()

# --- INTERFACE PRINCIPAL ---
st.title("🏥 Ficha de Avaliação Podológica")
st.markdown("---")
st.subheader("Profissional Responsável: **Elaine Souza**")

menu = ["Cadastrar Novo Paciente", "Consultar Histórico"]
choice = st.sidebar.selectbox("Menu de Opções", menu)

# Listas para os campos de múltipla escolha
lista_trabalha = ["Em pé", "Sentado", "Andando", "Destro", "Canhoto"]
lista_saude = [
    "Diabetes", "Hipertensão", "Cardíaco", "Anidrose", "Bromidrose", 
    "Pé Cavo", "Pé Plano", "Pé Equino Onicogrifose", "Halux Valgus D-E", 
    "Halux Varo D-E", "Calo Dorsal", "Calo de Milet", "Calo Subungueal", 
    "Calo Periungueal", "Calo Interdigital", "Onicofose", "Calo Duro", 
    "Calo Mole", "Calo Miliar", "Calo Vascular", "Calo Neuro Vascular", 
    "Calosidade", "Onicomicose"
]

if choice == "Cadastrar Novo Paciente":
    with st.form("ficha_form", clear_on_submit=True):
        st.markdown("### 👤 Informações Pessoais")
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome Completo:")
        data_nasc = c2.text_input("Data de Nascimento (DD/MM/AAAA):")
        endereco = c1.text_input("Endereço:")
        bairro = c2.text_input("Bairro:")
        cidade = c1.text_input("Cidade:")
        cep = c2.text_input("CEP:")
        telefone = c1.text_input("Telefone:")
        profissao = c2.text_input("Profissão:")

        st.markdown("---")
        st.markdown("### 👟 Estilo de Vida e Saúde")
        c3, c4 = st.columns(2)
        trabalha = c3.multiselect("Trabalha:", lista_trabalha)
        esporte = c4.radio("Pratica algum esporte?", ["Não", "Sim"], horizontal=True)
        calcado = c3.text_input("Calçado preferido?")
        cirurgia = c4.radio("Cirurgias anteriores no pé?", ["Não", "Sim"], horizontal=True)
        usa_med = c3.radio("Usa medicamentos?", ["Não", "Sim"], horizontal=True)
        quais_med = c4.text_area("Se usa medicamentos, quais?")

        st.markdown("---")
        st.markdown("### 🩹 Tratamento e Curativos")
        st.write("Curativos:")
        cur_cols = st.columns(5)
        cur1 = cur_cols[0].text_input("1º")
        cur2 = cur_cols[1].text_input("2º")
        cur3 = cur_cols[2].text_input("3º")
        cur4 = cur_cols[3].text_input("4º")
        cur5 = cur_cols[4].text_input("5º")

        c5, c6 = st.columns(2)
        granuloma = c5.text_input("Granuloma telangiectásico:")
        ortese = c6.text_input("Órtese:")
        artelho = c5.text_input("Artelho:")
        inicio = c6.text_input("Início do Tratamento:")
        final = c5.text_input("Final do Tratamento:")

        st.markdown("---")
        st.markdown("### 🩺 Avaliação Clínica (Assinale as opções)")
        condicoes_selecionadas = st.multiselect("Selecione todas as condições que o paciente apresenta:", lista_saude)

        st.markdown("---")
        st.markdown("### 🖋️ Validação e Assinatura")
        c_ass1, c_ass2 = st.columns(2)
        ass_paciente = c_ass1.text_input("Assinatura do Paciente (Nome):")
        # Campo bloqueado da profissional
        st.text_input("Profissional Responsável:", value="Elaine Souza", disabled=True)

        enviar = st.form_submit_button("SALVAR FICHA DE AVALIAÇÃO")

        if enviar:
            if nome:
                dados = {
                    "nome": nome, "data_nasc": data_nasc, "endereco": endereco, "telefone": telefone,
                    "bairro": bairro, "cidade": cidade, "cep": cep, "profissao": profissao,
                    "trabalha": ", ".join(trabalha), "esporte": esporte, "calcado": calcado,
                    "cirurgia": cirurgia, "medicamentos": usa_med, "medicamentos_quais": quais_med,
                    "curativo1": cur1, "curativo2": cur2, "curativo3": cur3, "curativo4": cur4, "curativo5": cur5,
                    "granuloma": granuloma, "ortese": ortese, "artelho": artelho,
                    "inicio": inicio, "final": final, "condicoes": ", ".join(condicoes_selecionadas),
                    "ass_paciente": ass_paciente, "profissional": "Elaine Souza"
                }
                salvar_dados(dados)
                st.success(f"✅ Ficha de {nome} salva com sucesso!")
            else:
                st.error("⚠️ Por favor, preencha pelo menos o nome do paciente.")

elif choice == "Consultar Histórico":
    st.markdown("### 🔍 Consulta de Pacientes Cadastrados")
    conn = sqlite3.connect('podologia_elaine.db')
    df = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()

    if not df.empty:
        # Busca por nome
        busca = st.text_input("Buscar paciente pelo nome:")
        if busca:
            df = df[df['nome'].str.contains(busca, case=False)]
        
        st.dataframe(df)
    else:
        st.info("Nenhum paciente cadastrado até o momento.")