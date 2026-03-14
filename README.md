## Simulador de Provas

Aplicação simples em **Streamlit** para importar questões em JSON, armazená-las em SQLite e realizar simulados com relatório de desempenho.

### Estrutura

- **database.py**: conexão com SQLite, criação da tabela `questoes` e funções utilitárias.
- **simulador.py**: página inicial com mensagem de boas-vindas e total de questões cadastradas.
- **pages/1_Importar.py**: tela para colar JSON de questões e salvar no banco.
- **pages/2_Simulado.py**: tela de simulado, cálculo de nota e relatório por questão.

### Executando o projeto

1. Crie e ative um ambiente virtual (opcional, mas recomendado).
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute o Streamlit:

   ```bash
   streamlit run simulador.py
   ```

# simulador-de-provas
Essa é uma aplicação que tem a finalidade de simular provas para concursos. Deve ser configurável para que possa se adequar a qualquer um(ou pelo menos a maioria) dos formato utilizados pelas bancas de concursos.
