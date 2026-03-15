import streamlit as st

from simulado_page import render_simulado


def main() -> None:
    st.title("Simulado")
    render_simulado()


if __name__ == "__main__":
    main()

