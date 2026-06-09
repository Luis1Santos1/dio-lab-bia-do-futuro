# Aplicacao Funcional

Aplicacao Streamlit do agente financeiro pessoal do Luis Rosa.

## O que ela faz

- Carrega a base local da pasta `data`.
- Calcula entradas, saidas, saldo previsto, cartao e maiores categorias.
- Exibe dashboard financeiro e chat interativo.
- Usa Ollama por padrao com modelo `gpt-oss`.
- Mantem fallback local baseado em regras caso a LLM esteja indisponivel.

## Como rodar com Ollama

1. Instale as dependencias:

```bash
pip install -r src/requirements.txt
```

2. Baixe o modelo no Ollama:

```bash
ollama pull gpt-oss
```

Se o seu Ollama usar um nome com tag, como `gpt-oss:20b`, coloque esse nome no `.env`.

3. Crie o arquivo `.env` na raiz do projeto:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=gpt-oss
```

4. Garanta que o Ollama esteja rodando:

```bash
ollama serve
```

5. Execute o app:

```bash
streamlit run src/app.py
```

## Como rodar com OpenAI opcionalmente

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini
```

Depois execute:

```bash
streamlit run src/app.py
```
