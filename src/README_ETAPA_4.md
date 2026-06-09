# Etapa 4 - Aplicacao Funcional

Este projeto entrega um prototipo funcional de um agente financeiro pessoal usando Streamlit, dados locais e LLM local via Ollama.

## Entregas da aplicacao

- Chatbot interativo em Streamlit.
- Dashboard com entradas, saidas, saldo previsto e cartao.
- Leitura da base de conhecimento em CSV e JSON.
- Analise de categorias de gasto e metas financeiras.
- Integracao padrao com Ollama usando modelo `gpt-oss`.
- Fallback local baseado em regras caso o Ollama esteja indisponivel.

## Estrutura esperada

```text
.
|-- data
|   |-- historico_atendimento_luis_rosa.csv
|   |-- perfil_investidor_luis_rosa.json
|   |-- produtos_financeiros_luis_rosa.json
|   `-- transacoes_luis_rosa.csv
|-- src
|   |-- app.py
|   |-- README.md
|   `-- requirements.txt
|-- .env.example
`-- README.md
```

## Como executar com Ollama

```bash
pip install -r src/requirements.txt
ollama pull gpt-oss
streamlit run src/app.py
```

Se necessario, crie um arquivo `.env` na raiz:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=gpt-oss
```

Caso o modelo local tenha tag, ajuste `OLLAMA_MODEL`, por exemplo:

```env
OLLAMA_MODEL=gpt-oss:20b
```

## OpenAI como alternativa

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini
```

## Observacao

O prototipo nao acessa banco, internet banking ou saldo bancario em tempo real. Ele usa somente os arquivos da pasta `data` e deixa claro quando uma informacao nao existe na base.
