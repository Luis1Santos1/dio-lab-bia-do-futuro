# Etapa 4 — Aplicação Funcional

Este arquivo implementa um protótipo funcional do agente financeiro pessoal do Luis Rosa usando Streamlit.

## O que a aplicação entrega

- Chatbot interativo em Streamlit.
- Carregamento da base de conhecimento da pasta `data`.
- Leitura de arquivos CSV e JSON.
- Análise de entradas, saídas, saldo previsto, cartão e categorias.
- Integração opcional com LLM via OpenAI.
- Fallback local baseado em regras caso não exista `OPENAI_API_KEY`.

## Estrutura esperada

```text
.
├── data
│   ├── historico_atendimento_luis_rosa.csv
│   ├── perfil_investidor_luis_rosa.json
│   ├── produtos_financeiros_luis_rosa.json
│   └── transacoes_luis_rosa.csv
├── src
│   └── app.py
├── requirements.txt
└── .env.example
```

A aplicação também aceita os nomes originais do desafio:

```text
historico_atendimento.csv
perfil_investidor.json
produtos_financeiros.json
transacoes.csv
```

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o app:

```bash
streamlit run src/app.py
```

## Uso com LLM

Para usar a integração com LLM, crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini
```

Sem a chave, o app continua funcionando com respostas locais baseadas nos dados carregados.

## Observação

Este protótipo não acessa banco, internet banking ou saldo bancário em tempo real.
Ele usa somente os arquivos da pasta `data`.
