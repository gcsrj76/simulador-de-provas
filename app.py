import streamlit as st


st.set_page_config(page_title="Simulador de Provas", page_icon="📝", layout="centered")


home_page = st.Page(
    "simulador.py",
    title="Home",
    icon="🏠",
)

importar_page = st.Page(
    "pages/1_Importar.py",
    title="Importar",
    icon="📥",
)

banco_questoes_page = st.Page(
    "pages/3_Banco de Questoes.py",
    title="Banco de Questões",
    icon="📚",
)


navigation = st.navigation(
    {
        "Simulador": [home_page],
        "Ferramentas": [importar_page, banco_questoes_page],
    }
)

navigation.run()

