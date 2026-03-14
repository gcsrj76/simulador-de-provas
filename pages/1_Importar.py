import json
from typing import Any

import streamlit as st

from database import salvar_questoes


def _validar_questao(q: dict[str, Any]) -> bool:
    campos_obrigatorios = [
        "pergunta",
        "opcao_a",
        "opcao_b",
        "opcao_c",
        "opcao_d",
        "correta",
        "dica",
        "link_conteudo",
    ]
    return all(campo in q and str(q[campo]).strip() for campo in campos_obrigatorios)


def main() -> None:
    st.title("Importar Questões")
    st.markdown(
        """
        Cole abaixo um **JSON** com uma **lista de questões**.

        Cada questão deve seguir o formato:

        ```json
        [
          {
            "pergunta": "Texto da pergunta",
            "opcao_a": "Opção A",
            "opcao_b": "Opção B",
            "opcao_c": "Opção C",
            "opcao_d": "Opção D",
            "correta": "a",
            "dica": "Dica para a questão",
            "link_conteudo": "https://link-para-estudo.com"
          }
        ]
        ```
        """
    )

    texto_json = st.text_area("Cole aqui o JSON das questões", height=300)

    if st.button("Salvar questões no banco"):
        if not texto_json.strip():
            st.warning("Cole o JSON antes de salvar.")
            return

        try:
            dados = json.loads(texto_json)
        except json.JSONDecodeError as exc:
            st.error(f"JSON inválido: {exc}")
            return

        if not isinstance(dados, list):
            st.error("O JSON deve ser uma **lista de questões**.")
            return

        questoes_validas = [q for q in dados if isinstance(q, dict) and _validar_questao(q)]

        if not questoes_validas:
            st.error(
                "Nenhuma questão válida encontrada. "
                "Verifique se todas possuem os campos obrigatórios."
            )
            return

        try:
            inseridas = salvar_questoes(questoes_validas)
        except Exception as exc:
            st.error(f"Erro ao salvar questões no banco: {exc}")
            return

        st.success(f"{inseridas} questão(ões) cadastrada(s) com sucesso!")


if __name__ == "__main__":
    main()

