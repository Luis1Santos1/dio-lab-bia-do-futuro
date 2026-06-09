# Etapa 4 - Aplicacao Funcional

## Arquivo principal

`src/app.py`

## Resumo

A aplicacao funcional foi implementada em Streamlit e esta pronta para rodar localmente com Ollama.

Principais pontos:

- Carrega a base da pasta `data`.
- Le arquivos CSV e JSON.
- Calcula resumo financeiro do mes.
- Exibe dashboard com entradas, saidas, saldo previsto, cartao e categorias.
- Disponibiliza chat com historico da conversa.
- Usa `LLM_PROVIDER=ollama` por padrao.
- Usa `OLLAMA_MODEL=gpt-oss` por padrao.
- Permite alternativa com OpenAI por configuracao.
- Mantem fallback local caso a LLM nao esteja disponivel.

## Como executar

```bash
pip install -r src/requirements.txt
ollama pull gpt-oss
streamlit run src/app.py
```

Se o modelo local tiver tag, configure no `.env`:

```env
OLLAMA_MODEL=gpt-oss:20b
```

## Observacao

O codigo completo esta em `src/app.py`. Este documento evita duplicar o codigo para nao ficar desatualizado quando a aplicacao evoluir.
