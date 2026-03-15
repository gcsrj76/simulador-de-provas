from typing import Any

import streamlit as st

from database import listar_questoes


def _calcular_nota(acertos: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((acertos / total) * 10, 2)


def render_simulado() -> None:
    st.subheader("Simulado")

    questoes = listar_questoes()

    if not questoes:
        st.info("Nenhuma questão cadastrada. Importe questões antes de realizar o simulado.")
        return

    st.markdown("Responda às questões abaixo e clique em **Finalizar simulado**.")

    respostas: dict[int, str] = {}
    for idx, q in enumerate(questoes, start=1):
        st.markdown(f"### Questão {idx}")
        texto_referencia = str(q.get("texto_referencia") or "").strip()
        if texto_referencia:
            st.info(texto_referencia)

        link_conteudo = str(q.get("link_conteudo") or "").strip()
        col_pergunta, col_botao = st.columns([4, 1])
        with col_pergunta:
            st.write(q["pergunta"])
        with col_botao:
            if link_conteudo:
                st.link_button("Abrir link", url=link_conteudo)

        opcoes = {
            "a": q["opcao_a"],
            "b": q["opcao_b"],
            "c": q["opcao_c"],
            "d": q["opcao_d"],
        }

        escolha = st.radio(
            "Selecione uma alternativa:",
            options=list(opcoes.keys()),
            format_func=lambda x, m=opcoes: f"{x.upper()}) {m[x]}",
            key=f"q_{q['id']}",
            index=None,
        )
        respostas[q["id"]] = escolha

        st.markdown("---")

    submitted = st.button("Finalizar simulado")

    if not submitted:
        return

    acertos = 0
    resultados: list[dict[str, Any]] = []

    for q in questoes:
        correta = str(q["correta"]).strip().lower()
        resp_usuario = str(respostas.get(q["id"], "")).lower()
        correto = resp_usuario == correta
        if correto:
            acertos += 1

        resultados.append(
            {
                "pergunta": q["pergunta"],
                "correta": correta,
                "resp_usuario": resp_usuario,
                "link_conteudo": q.get("link_conteudo", ""),
                "opcoes": {
                    "a": q["opcao_a"],
                    "b": q["opcao_b"],
                    "c": q["opcao_c"],
                    "d": q["opcao_d"],
                },
                "correto": correto,
            }
        )

    total = len(questoes)
    nota = _calcular_nota(acertos, total)

    st.subheader("Resultado do Simulado")
    st.write(f"Você acertou **{acertos}** de **{total}** questões.")
    st.write(f"Sua nota final foi: **{nota} / 10**.")

    st.markdown("---")
    st.subheader("Relatório por questão")

    for idx, r in enumerate(resultados, start=1):
        status = "✅ Acertou" if r["correto"] else "❌ Errou"
        st.markdown(f"**Questão {idx}: {status}**")
        st.write(r["pergunta"])

        opcoes = r["opcoes"]
        st.markdown(
            "\n".join(
                [
                    f"- A) {opcoes['a']}",
                    f"- B) {opcoes['b']}",
                    f"- C) {opcoes['c']}",
                    f"- D) {opcoes['d']}",
                ]
            )
        )

        if r["resp_usuario"]:
            st.write(f"Sua resposta: **{r['resp_usuario'].upper()}**")
        else:
            st.write("Você **não respondeu** esta questão.")

        st.write(f"Resposta correta: **{r['correta'].upper()}**")

        if r["link_conteudo"]:
            st.markdown(f"[Estudar o conteúdo da questão]({r['link_conteudo']})")

        st.markdown("---")

