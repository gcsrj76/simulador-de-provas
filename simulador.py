import streamlit as st

from database import contar_questoes
from simulado_page import render_simulado


st.set_page_config(page_title="Simulador de Provas", page_icon="📝", layout="centered")


def _init_state() -> None:
    if "mostrar_simulado_home" not in st.session_state:
        st.session_state["mostrar_simulado_home"] = False


def main() -> None:
    _init_state()

    if not st.session_state["mostrar_simulado_home"]:
        # Tela principal (Home)
        st.title("Simulador de Provas")
        st.markdown(
            """
            Bem-vindo ao **Simulador de Provas**!  
            Use o menu lateral para **Importar**, gerenciar o **Banco de Questões**
            ou acessar o **Simulado**.
            """
        )

        try:
            total = contar_questoes()
        except Exception as exc:  # proteção básica para erros inesperados
            st.error(f"Erro ao carregar total de questões: {exc}")
            total = 0

        st.metric("Total de questões cadastradas", total)

        st.markdown("---")
        if st.button("Simulado"):
            st.session_state["mostrar_simulado_home"] = True
            st.rerun()
    else:
        # Tela do Simulado ocupando a página
        st.title("Simulado")
        if st.button("Voltar"):
            st.session_state["mostrar_simulado_home"] = False
            st.rerun()

        render_simulado()


if __name__ == "__main__":
    main()



