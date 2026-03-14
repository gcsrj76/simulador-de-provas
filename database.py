import sqlite3
from typing import Iterable, Mapping, Any


DB_PATH = "questoes.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    _criar_tabela_questoes(conn)
    return conn


def _criar_tabela_questoes(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS questoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT NOT NULL,
            opcao_a TEXT NOT NULL,
            opcao_b TEXT NOT NULL,
            opcao_c TEXT NOT NULL,
            opcao_d TEXT NOT NULL,
            correta TEXT NOT NULL,
            dica TEXT,
            link_conteudo TEXT
        )
        """
    )
    conn.commit()


def salvar_questoes(questoes: Iterable[Mapping[str, Any]]) -> int:
    """
    Salva uma lista de questões no banco.

    Cada questão deve conter as chaves:
    pergunta, opcao_a, opcao_b, opcao_c, opcao_d, correta, dica, link_conteudo.
    Retorna o número de questões inseridas.
    """
    conn = get_connection()
    cursor = conn.cursor()

    dados = []
    for q in questoes:
        dados.append(
            (
                q.get("pergunta", "").strip(),
                q.get("opcao_a", "").strip(),
                q.get("opcao_b", "").strip(),
                q.get("opcao_c", "").strip(),
                q.get("opcao_d", "").strip(),
                q.get("correta", "").strip(),
                q.get("dica", "").strip(),
                q.get("link_conteudo", "").strip(),
            )
        )

    cursor.executemany(
        """
        INSERT INTO questoes (
            pergunta, opcao_a, opcao_b, opcao_c, opcao_d, correta, dica, link_conteudo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        dados,
    )
    conn.commit()
    inseridas = cursor.rowcount
    conn.close()
    return inseridas


def contar_questoes() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM questoes")
    total = cursor.fetchone()[0]
    conn.close()
    return int(total)


def listar_questoes() -> list[dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id, pergunta, opcao_a, opcao_b, opcao_c, opcao_d,
            correta, dica, link_conteudo
        FROM questoes
        ORDER BY id
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

