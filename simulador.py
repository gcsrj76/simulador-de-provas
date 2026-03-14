import streamlit as st

from database import contar_questoes


st.set_page_config(page_title="Simulador de Provas", page_icon="📝", layout="centered")


def main() -> None:
    st.title("Simulador de Provas")
    st.markdown(
        """
        Bem-vindo ao **Simulador de Provas**!  
        Use o menu lateral para **importar questões** ou **realizar um simulado**.
        """
    )

    try:
        total = contar_questoes()
    except Exception as exc:  # proteção básica para erros inesperados
        st.error(f"Erro ao carregar total de questões: {exc}")
        total = 0

    st.metric("Total de questões cadastradas", total)


if __name__ == "__main__":
    main()

