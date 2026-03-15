import streamlit as st

from database import listar_questoes, inserir_questao, atualizar_questao, deletar_questao


def _init_state() -> None:
    if "crud_modo" not in st.session_state:
        st.session_state["crud_modo"] = "edicao"  # ou "novo"
    if "crud_selected_id" not in st.session_state:
        st.session_state["crud_selected_id"] = None
    if "crud_initialized" not in st.session_state:
        st.session_state["crud_initialized"] = False


def _set_form_from_dict(dados: dict) -> None:
    st.session_state["crud_pergunta"] = dados.get("pergunta", "")
    st.session_state["crud_opcao_a"] = dados.get("opcao_a", "")
    st.session_state["crud_opcao_b"] = dados.get("opcao_b", "")
    st.session_state["crud_opcao_c"] = dados.get("opcao_c", "")
    st.session_state["crud_opcao_d"] = dados.get("opcao_d", "")
    st.session_state["crud_correta"] = str(dados.get("correta", "a")).lower() or "a"
    st.session_state["crud_link_conteudo"] = dados.get("link_conteudo", "")
    st.session_state["crud_texto_referencia"] = dados.get("texto_referencia", "")
    st.session_state["crud_materia"] = dados.get("materia", "")


def _build_form() -> dict:
    st.subheader("Dados da questão")

    pergunta = st.text_area("Pergunta", key="crud_pergunta", height=120)
    col_a, col_b = st.columns(2)
    with col_a:
        opcao_a = st.text_input("Opção A", key="crud_opcao_a")
        opcao_c = st.text_input("Opção C", key="crud_opcao_c")
    with col_b:
        opcao_b = st.text_input("Opção B", key="crud_opcao_b")
        opcao_d = st.text_input("Opção D", key="crud_opcao_d")

    correta = st.selectbox(
        "Alternativa correta",
        options=["a", "b", "c", "d"],
        key="crud_correta",
    )

    link_conteudo = st.text_input(
        "Link para conteúdo (opcional)", key="crud_link_conteudo"
    )
    texto_referencia = st.text_area(
        "Texto de referência (opcional)",
        key="crud_texto_referencia",
        height=80,
    )
    materia = st.text_input("Matéria (opcional)", key="crud_materia")

    return {
        "pergunta": pergunta,
        "opcao_a": opcao_a,
        "opcao_b": opcao_b,
        "opcao_c": opcao_c,
        "opcao_d": opcao_d,
        "correta": correta,
        "link_conteudo": link_conteudo,
        "texto_referencia": texto_referencia,
        "materia": materia,
    }


def main() -> None:
    st.title("Banco de Questões")
    st.markdown(
        "Visualize, inclua, edite e remova questões diretamente da base de dados."
    )

    _init_state()

    questoes = listar_questoes()

    # Dados para exibição da tabela com coluna de seleção
    dados_tabela = [
        {
            "Selecionar": q["id"] == st.session_state["crud_selected_id"],
            "id": q["id"],
            "pergunta": q.get("pergunta", ""),
            "opcao_a": q.get("opcao_a", ""),
            "opcao_b": q.get("opcao_b", ""),
            "opcao_c": q.get("opcao_c", ""),
            "opcao_d": q.get("opcao_d", ""),
            "correta": q.get("correta", ""),
            "link_conteudo": q.get("link_conteudo", ""),
            "texto_referencia": q.get("texto_referencia", ""),
        }
        for q in questoes
    ]

    # Barra de botões acima da tabela
    col_del, col_add, col_save = st.columns([1, 1, 1])
    excluir_clicked = col_del.button("Excluir")
    incluir_clicked = col_add.button("Incluir")
    gravar_clicked = col_save.button("Gravar")

    # Tabela sempre visível, largura total, com scroll horizontal automático
    tabela_editada = st.data_editor(
        dados_tabela,
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        key="crud_tabela",
    )

    # Verifica qual linha foi marcada na coluna "Selecionar"
    selected_ids = [
        linha["id"] for linha in tabela_editada if linha.get("Selecionar")
    ]
    selected_id = selected_ids[0] if selected_ids else None

    # Atualiza seleção conforme estado dos checkboxes
    if selected_id is not None:
        # Houve uma linha marcada
        if selected_id != st.session_state["crud_selected_id"]:
            st.session_state["crud_selected_id"] = selected_id
            st.session_state["crud_modo"] = "edicao"
            registro = next((q for q in questoes if q["id"] == selected_id), None) or {}
            _set_form_from_dict(registro)
    else:
        # Nenhuma linha marcada: limpa a seleção sem re-selecionar automaticamente
        if st.session_state["crud_selected_id"] is not None:
            st.session_state["crud_selected_id"] = None

    # Na primeira carga, se ainda não inicializado e houver registros, seleciona o primeiro
    if (
        not st.session_state["crud_initialized"]
        and st.session_state["crud_selected_id"] is None
        and questoes
        and st.session_state["crud_modo"] == "edicao"
    ):
        primeira = questoes[0]
        st.session_state["crud_selected_id"] = primeira["id"]
        _set_form_from_dict(primeira)
        st.session_state["crud_initialized"] = True

    # Comportamento dos botões de ação
    if incluir_clicked:
        # Prepara formulário para nova questão
        st.session_state["crud_modo"] = "novo"
        st.session_state["crud_selected_id"] = None
        _set_form_from_dict({})

    if excluir_clicked and st.session_state["crud_modo"] == "edicao":
        if st.session_state["crud_selected_id"] is not None:
            deletar_questao(st.session_state["crud_selected_id"])
            st.success("Questão excluída com sucesso.")
            st.session_state["crud_selected_id"] = None
            _set_form_from_dict({})
            st.rerun()
        else:
            st.warning("Selecione uma questão na tabela para excluir.")

    # Formulário sempre na parte inferior, ocupando toda a largura
    dados_form = _build_form()

    if gravar_clicked:
        if st.session_state["crud_modo"] == "novo":
            novo_id = inserir_questao(dados_form)
            st.success(f"Questão incluída com sucesso (ID {novo_id}).")
            st.session_state["crud_selected_id"] = novo_id
            st.session_state["crud_modo"] = "edicao"
            st.rerun()
        else:
            if st.session_state["crud_selected_id"] is None:
                st.warning("Selecione uma questão na tabela para salvar alterações.")
            else:
                atualizar_questao(st.session_state["crud_selected_id"], dados_form)
                st.success("Questão atualizada com sucesso.")
                st.rerun()


if __name__ == "__main__":
    main()

