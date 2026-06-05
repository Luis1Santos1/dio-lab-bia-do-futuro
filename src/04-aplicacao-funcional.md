# Etapa 4 — Aplicação Funcional

## Arquivo principal

`src/app.py`

## Código

```python
import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================

APP_TITLE = "Assistente Financeiro | Luis Rosa"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# A aplicação aceita tanto os nomes originais do desafio quanto os arquivos ajustados.
FILE_CANDIDATES = {
    "perfil": [
        "perfil_investidor_luis_rosa.json",
        "perfil_investidor.json",
    ],
    "transacoes": [
        "transacoes_luis_rosa.csv",
        "transacoes.csv",
    ],
    "historico": [
        "historico_atendimento_luis_rosa.csv",
        "historico_atendimento.csv",
    ],
    "produtos": [
        "produtos_financeiros_luis_rosa.json",
        "produtos_financeiros.json",
    ],
}


# ============================================================
# FUNÇÕES DE SUPORTE
# ============================================================

def normalize_text(value: Any) -> str:
    """Normaliza texto para buscas simples sem acento e sem case sensitive."""
    if value is None:
        return ""

    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text


def format_currency(value: Any) -> str:
    """Formata números em Real brasileiro."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "R$ 0,00"

    formatted = f"R$ {number:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def parse_money(value: Any) -> float:
    """Converte valores monetários em float, aceitando padrões BR e US."""
    if pd.isna(value):
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    text = text.replace("R$", "").replace(" ", "")

    # Caso brasileiro: 1.234,56
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    # Caso brasileiro simples: 1234,56
    elif "," in text:
        text = text.replace(",", ".")

    text = re.sub(r"[^0-9\-.]", "", text)

    try:
        return float(text)
    except ValueError:
        return 0.0


def find_project_root() -> Path:
    """
    Procura a raiz do projeto.
    Esperado:
    - raiz/data
    - raiz/src/app.py

    Também funciona se o app.py for executado diretamente.
    """
    current = Path(__file__).resolve()

    for parent in [current.parent, *current.parents]:
        if (parent / "data").exists():
            return parent

    return current.parent.parent


def find_file(data_path: Path, candidates: List[str]) -> Optional[Path]:
    for filename in candidates:
        path = data_path / filename
        if path.exists():
            return path

    return None


@st.cache_data(show_spinner=False)
def load_json(path: Optional[Path]) -> Any:
    if path is None:
        return None

    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


@st.cache_data(show_spinner=False)
def load_csv(path: Optional[Path]) -> pd.DataFrame:
    if path is None:
        return pd.DataFrame()

    encodings = ["utf-8-sig", "utf-8", "latin1"]

    for encoding in encodings:
        try:
            return pd.read_csv(path, encoding=encoding, sep=None, engine="python")
        except Exception:
            continue

    return pd.DataFrame()


def load_knowledge_base() -> Tuple[Dict[str, Any], Dict[str, Optional[Path]]]:
    root = find_project_root()
    data_path = root / "data"

    paths = {
        key: find_file(data_path, candidates)
        for key, candidates in FILE_CANDIDATES.items()
    }

    knowledge = {
        "perfil": load_json(paths["perfil"]) or {},
        "transacoes": load_csv(paths["transacoes"]),
        "historico": load_csv(paths["historico"]),
        "produtos": load_json(paths["produtos"]) or [],
    }

    return knowledge, paths


# ============================================================
# ANÁLISES FINANCEIRAS
# ============================================================

def prepare_transactions(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    prepared = df.copy()
    prepared.columns = [normalize_text(col).replace(" ", "_") for col in prepared.columns]

    # Colunas esperadas: data, descricao, categoria, valor, tipo.
    if "valor" in prepared.columns:
        prepared["valor_num"] = prepared["valor"].apply(parse_money)
    else:
        prepared["valor_num"] = 0.0

    if "tipo" not in prepared.columns:
        prepared["tipo"] = ""

    if "categoria" not in prepared.columns:
        prepared["categoria"] = "Sem categoria"

    if "descricao" not in prepared.columns:
        prepared["descricao"] = ""

    prepared["tipo_norm"] = prepared["tipo"].apply(normalize_text)
    prepared["categoria_norm"] = prepared["categoria"].apply(normalize_text)
    prepared["descricao_norm"] = prepared["descricao"].apply(normalize_text)

    return prepared


def build_financial_summary(perfil: Dict[str, Any], transacoes: pd.DataFrame) -> Dict[str, Any]:
    df = prepare_transactions(transacoes)

    if df.empty:
        indicadores = perfil.get("indicadores_mes_atual", {}) if isinstance(perfil, dict) else {}
        return {
            "entradas": indicadores.get("entradas_previstas", 0),
            "saidas": indicadores.get("saidas_previstas", 0),
            "saldo": indicadores.get("saldo_previsto", 0),
            "cartoes": indicadores.get("cartoes_no_mes", 0),
            "top_categorias": [],
            "top_despesas": [],
            "diagnostico": indicadores.get("diagnostico", "Sem diagnóstico calculado"),
        }

    entradas_df = df[df["tipo_norm"].isin(["entrada", "receita", "receber"])]
    saidas_df = df[df["tipo_norm"].isin(["saida", "despesa", "pagar"])]

    entradas = float(entradas_df["valor_num"].sum())
    saidas = float(saidas_df["valor_num"].sum())
    saldo = entradas - saidas

    cartao_mask = (
        saidas_df["descricao_norm"].str.contains("cartao|cartão", regex=True, na=False)
        | saidas_df["categoria_norm"].str.contains("cartao|cartão|fatura", regex=True, na=False)
    )
    cartoes = float(saidas_df[cartao_mask]["valor_num"].sum())

    top_categorias = (
        saidas_df.groupby("categoria", dropna=False)["valor_num"]
        .sum()
        .sort_values(ascending=False)
        .head(8)
        .reset_index()
        .to_dict(orient="records")
    )

    top_despesas = (
        saidas_df.sort_values("valor_num", ascending=False)
        .head(10)[["descricao", "categoria", "valor_num"]]
        .to_dict(orient="records")
    )

    if saldo < 0:
        diagnostico = "Atenção: mês negativo"
    elif saidas > 0 and saldo / max(entradas, 1) < 0.1:
        diagnostico = "Atenção: sobra mensal baixa"
    else:
        diagnostico = "Mês positivo, mas ainda exige acompanhamento"

    return {
        "entradas": entradas,
        "saidas": saidas,
        "saldo": saldo,
        "cartoes": cartoes,
        "top_categorias": top_categorias,
        "top_despesas": top_despesas,
        "diagnostico": diagnostico,
    }


def get_goals(perfil: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not isinstance(perfil, dict):
        return []

    metas = perfil.get("metas", [])
    return metas if isinstance(metas, list) else []


def build_context_text(
    perfil: Dict[str, Any],
    summary: Dict[str, Any],
    historico: pd.DataFrame,
    produtos: List[Dict[str, Any]],
) -> str:
    metas = get_goals(perfil)

    historico_text = "Nenhum histórico carregado."
    if not historico.empty:
        recent_cols = [col for col in historico.columns if col in ["data", "tema", "resumo", "resolvido"]]
        if recent_cols:
            historico_text = historico[recent_cols].tail(5).to_string(index=False)
        else:
            historico_text = historico.tail(5).to_string(index=False)

    produtos_text = "Nenhum produto carregado."
    if isinstance(produtos, list) and produtos:
        produtos_text = "\n".join(
            f"- {item.get('nome', 'Produto sem nome')} | risco: {item.get('risco', 'n/a')} | indicado para: {item.get('indicado_para', 'n/a')}"
            for item in produtos[:8]
            if isinstance(item, dict)
        )

    metas_text = "Nenhuma meta cadastrada."
    if metas:
        metas_text = "\n".join(
            f"- {meta.get('meta', 'Meta sem nome')}: {format_currency(meta.get('valor_necessario', 0))} até {meta.get('prazo', 'sem prazo')}"
            for meta in metas[:8]
        )

    top_categorias_text = "\n".join(
        f"- {item.get('categoria', 'Sem categoria')}: {format_currency(item.get('valor_num', 0))}"
        for item in summary.get("top_categorias", [])
    ) or "Sem categorias calculadas."

    return f"""
DADOS DO CLIENTE
- Nome: {perfil.get("nome", "Luis Rosa")}
- Profissão: {perfil.get("profissao", "Não informado")}
- Perfil financeiro/investidor: {perfil.get("perfil_investidor", "Não informado")}
- Objetivo principal: {perfil.get("objetivo_principal", "Organização financeira pessoal")}
- Aceita risco: {perfil.get("aceita_risco", "Não informado")}

RESUMO FINANCEIRO CALCULADO
- Entradas: {format_currency(summary.get("entradas", 0))}
- Saídas: {format_currency(summary.get("saidas", 0))}
- Saldo previsto: {format_currency(summary.get("saldo", 0))}
- Cartões identificados: {format_currency(summary.get("cartoes", 0))}
- Diagnóstico: {summary.get("diagnostico", "Não calculado")}

MAIORES CATEGORIAS DE SAÍDA
{top_categorias_text}

METAS
{metas_text}

HISTÓRICO RECENTE DE ATENDIMENTO
{historico_text}

PRODUTOS FINANCEIROS DISPONÍVEIS PARA CONSULTA
{produtos_text}

REGRAS IMPORTANTES
- Não invente dados ausentes.
- Não trate os dados como saldo bancário em tempo real.
- Priorize organização financeira, controle de cartão e fluxo de caixa.
- Não recomende investimentos de risco se o mês estiver negativo ou sem reserva.
- Evite duplicar fatura do cartão com compras detalhadas.
""".strip()


# ============================================================
# PROMPT E RESPOSTA
# ============================================================

SYSTEM_PROMPT = """
Você é um agente financeiro pessoal especializado exclusivamente na organização financeira do Luis Rosa.

Seu objetivo é ajudar o Luis a entender, organizar e melhorar sua vida financeira com base nos dados fornecidos nos arquivos da pasta data.

Você deve atuar como um assistente financeiro prático, direto e confiável, focado em:
- controle de entradas e saídas;
- análise de gastos mensais;
- acompanhamento de contas a pagar e a receber;
- análise de cartão de crédito;
- identificação de categorias que mais pesam no orçamento;
- acompanhamento de metas financeiras;
- organização de dívidas e compromissos recorrentes;
- sugestão de ações simples para melhorar o fluxo de caixa.

Regras:
1. Sempre baseie suas respostas nos dados disponíveis.
2. Nunca invente valores, datas, saldos, dívidas, metas ou informações pessoais.
3. Se uma informação não estiver disponível, diga claramente que ela não consta na base.
4. Priorize organização financeira antes de sugerir investimentos.
5. Diferencie compras no cartão da fatura agregada para evitar duplicidade.
6. Não recomende novos compromissos financeiros sem avaliar o fluxo de caixa.
7. Não prometa rentabilidade.
8. Se o usuário pedir algo fora de finanças pessoais, explique que esse agente é focado em finanças.
9. Responda em português do Brasil, com linguagem simples, direta e prática.

Estrutura recomendada quando fizer análise:
1. Resumo rápido
2. Dados encontrados
3. Análise
4. Pontos de atenção
5. Próximas ações recomendadas
""".strip()


def get_openai_client() -> Optional[Any]:
    if load_dotenv:
        load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return None

    return OpenAI(api_key=api_key)


def generate_llm_answer(question: str, context: str, history: List[Dict[str, str]]) -> Optional[str]:
    client = get_openai_client()

    if client is None:
        return None

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Base de conhecimento carregada:\n\n{context}"},
    ]

    # Mantém apenas as últimas mensagens para evitar contexto grande demais.
    for item in history[-8:]:
        if item.get("role") in ["user", "assistant"]:
            messages.append({"role": item["role"], "content": item.get("content", "")})

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        temperature=0.2,
    )

    return response.choices[0].message.content


def fallback_answer(question: str, perfil: Dict[str, Any], summary: Dict[str, Any]) -> str:
    q = normalize_text(question)
    metas = get_goals(perfil)

    if any(term in q for term in ["cartao", "fatura", "credito"]):
        percentual = 0
        if summary.get("saidas", 0):
            percentual = summary.get("cartoes", 0) / summary.get("saidas", 1)

        return f"""
### Resumo rápido

O cartão precisa ser acompanhado de perto.

### Dados encontrados

- Saídas totais: **{format_currency(summary.get("saidas", 0))}**
- Gastos identificados como cartão: **{format_currency(summary.get("cartoes", 0))}**
- Peso aproximado do cartão nas saídas: **{percentual:.1%}**

### Análise

Se esse percentual estiver alto, o cartão pode estar reduzindo sua sobra mensal e aumentando o risco de fechar o mês negativo.

### Próximas ações recomendadas

1. Evitar novos parcelamentos temporariamente.
2. Separar compras essenciais de compras adiáveis.
3. Definir um teto mensal para cartão.
4. Acompanhar semanalmente a evolução da fatura.
5. Não somar fatura consolidada e compras detalhadas ao mesmo tempo para evitar duplicidade.
""".strip()

    if any(term in q for term in ["investir", "investimento", "aplicar", "tesouro", "cdb"]):
        return f"""
### Resumo rápido

Antes de investir, a prioridade é validar se existe sobra real no mês.

### Dados encontrados

- Entradas: **{format_currency(summary.get("entradas", 0))}**
- Saídas: **{format_currency(summary.get("saidas", 0))}**
- Saldo previsto: **{format_currency(summary.get("saldo", 0))}**
- Diagnóstico: **{summary.get("diagnostico", "Não calculado")}**

### Análise

Com esse cenário, o mais seguro é priorizar organização financeira, controle do cartão e formação de reserva de emergência antes de buscar investimentos com maior risco.

### Próximas ações recomendadas

1. Confirmar contas ainda em aberto.
2. Reduzir gastos variáveis e cartão.
3. Evitar novas dívidas.
4. Só investir se houver sobra real.
5. Se houver sobra, priorizar alternativas conservadoras e com liquidez.
""".strip()

    if any(term in q for term in ["gasto", "categoria", "onde estou gastando", "maiores"]):
        linhas = []
        for item in summary.get("top_categorias", [])[:5]:
            linhas.append(f"- **{item.get('categoria', 'Sem categoria')}**: {format_currency(item.get('valor_num', 0))}")

        categorias = "\n".join(linhas) or "Não consegui calcular as categorias com os dados disponíveis."

        return f"""
### Resumo rápido

As maiores categorias de saída ajudam a identificar onde o orçamento está sendo mais pressionado.

### Maiores categorias encontradas

{categorias}

### Análise

O ideal é começar os ajustes pelas categorias de maior impacto, principalmente quando forem gastos variáveis, cartão ou compras adiáveis.

### Próximas ações recomendadas

1. Revisar os maiores gastos do mês.
2. Separar essencial de não essencial.
3. Criar teto por categoria.
4. Acompanhar o cartão semanalmente.
""".strip()

    if any(term in q for term in ["meta", "guardar", "reserva", "objetivo"]):
        if metas:
            metas_text = "\n".join(
                f"- **{meta.get('meta', 'Meta sem nome')}**: {format_currency(meta.get('valor_necessario', 0))} até {meta.get('prazo', 'sem prazo')}"
                for meta in metas
            )
        else:
            metas_text = "Não encontrei metas cadastradas na base."

        return f"""
### Resumo rápido

Estas são as metas encontradas na base:

{metas_text}

### Análise

Para definir quanto guardar por mês, é necessário cruzar o valor necessário, o prazo e a sobra real mensal.

Saldo previsto atual: **{format_currency(summary.get("saldo", 0))}**

### Próximas ações recomendadas

1. Se o mês estiver negativo, priorizar reequilíbrio antes de aportes.
2. Se houver sobra, definir um valor mensal realista.
3. Revisar a meta todo mês.
4. Evitar metas agressivas enquanto o cartão estiver pressionando o orçamento.
""".strip()

    return f"""
### Resumo rápido

Com base na base financeira carregada, este é o cenário geral:

- Entradas: **{format_currency(summary.get("entradas", 0))}**
- Saídas: **{format_currency(summary.get("saidas", 0))}**
- Saldo previsto: **{format_currency(summary.get("saldo", 0))}**
- Cartões identificados: **{format_currency(summary.get("cartoes", 0))}**
- Diagnóstico: **{summary.get("diagnostico", "Não calculado")}**

### Pontos de atenção

1. Validar contas ainda pendentes.
2. Acompanhar cartão de crédito.
3. Evitar novas parcelas no curto prazo.
4. Não considerar investimento antes de confirmar sobra real.
5. Atualizar a base sempre que houver novas compras ou pagamentos.

### Próxima ação recomendada

Comece perguntando algo como:
- "Onde estou gastando mais?"
- "Meu cartão está alto?"
- "Posso investir esse mês?"
- "Quanto falta para fechar o mês?"
""".strip()


def answer_question(
    question: str,
    perfil: Dict[str, Any],
    summary: Dict[str, Any],
    context: str,
    history: List[Dict[str, str]],
) -> str:
    try:
        llm_answer = generate_llm_answer(question, context, history)
        if llm_answer:
            return llm_answer
    except Exception as exc:
        return f"""
Não consegui consultar a LLM neste momento.

Erro retornado:
`{exc}`

Mesmo assim, segue uma análise local com base nos dados carregados:

{fallback_answer(question, perfil, summary)}
""".strip()

    return fallback_answer(question, perfil, summary)


# ============================================================
# INTERFACE STREAMLIT
# ============================================================

def render_sidebar(paths: Dict[str, Optional[Path]], perfil: Dict[str, Any], summary: Dict[str, Any]) -> None:
    st.sidebar.title("Base carregada")

    for key, path in paths.items():
        if path:
            st.sidebar.success(f"{key}: {path.name}")
        else:
            st.sidebar.error(f"{key}: arquivo não encontrado")

    st.sidebar.divider()
    st.sidebar.subheader("Resumo do mês")

    st.sidebar.metric("Entradas", format_currency(summary.get("entradas", 0)))
    st.sidebar.metric("Saídas", format_currency(summary.get("saidas", 0)))
    st.sidebar.metric("Saldo previsto", format_currency(summary.get("saldo", 0)))
    st.sidebar.metric("Cartões", format_currency(summary.get("cartoes", 0)))

    st.sidebar.divider()
    st.sidebar.subheader("Perfil")

    st.sidebar.write(f"**Nome:** {perfil.get('nome', 'Luis Rosa')}")
    st.sidebar.write(f"**Perfil:** {perfil.get('perfil_investidor', 'Não informado')}")
    st.sidebar.write(f"**Objetivo:** {perfil.get('objetivo_principal', 'Organização financeira')}")


def render_dashboard(summary: Dict[str, Any]) -> None:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Entradas", format_currency(summary.get("entradas", 0)))
    col2.metric("Saídas", format_currency(summary.get("saidas", 0)))
    col3.metric("Saldo previsto", format_currency(summary.get("saldo", 0)))
    col4.metric("Cartões", format_currency(summary.get("cartoes", 0)))

    st.info(f"Diagnóstico: **{summary.get('diagnostico', 'Não calculado')}**")

    top_categorias = summary.get("top_categorias", [])
    if top_categorias:
        st.subheader("Maiores categorias de saída")
        chart_df = pd.DataFrame(top_categorias)
        chart_df = chart_df.rename(columns={"valor_num": "valor"})
        st.bar_chart(chart_df.set_index("categoria")["valor"])


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="💰", layout="wide")

    knowledge, paths = load_knowledge_base()

    perfil = knowledge["perfil"]
    transacoes = knowledge["transacoes"]
    historico = knowledge["historico"]
    produtos = knowledge["produtos"]

    summary = build_financial_summary(perfil, transacoes)
    context = build_context_text(perfil, summary, historico, produtos)

    render_sidebar(paths, perfil, summary)

    st.title("💰 Assistente Financeiro do Luis Rosa")
    st.write(
        "Chatbot funcional para consultar a base financeira, analisar gastos, cartão, metas e fluxo de caixa."
    )

    render_dashboard(summary)

    with st.expander("Ver contexto resumido enviado ao agente"):
        st.code(context, language="text")

    st.divider()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá, Luis! Posso te ajudar a analisar seus gastos, cartão, metas e saldo previsto com base nos arquivos da pasta data.",
            }
        ]

    st.subheader("Chat financeiro")

    suggestions = [
        "Como está minha situação financeira esse mês?",
        "Onde estou gastando mais?",
        "Meu cartão está muito alto?",
        "Posso investir esse mês?",
        "Quanto preciso guardar para minhas metas?",
    ]

    selected_suggestion = st.selectbox(
        "Perguntas rápidas",
        options=[""] + suggestions,
        index=0,
    )

    if selected_suggestion and st.button("Enviar pergunta rápida"):
        st.session_state.messages.append({"role": "user", "content": selected_suggestion})
        response = answer_question(
            selected_suggestion,
            perfil,
            summary,
            context,
            st.session_state.messages,
        )
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Pergunte algo sobre suas finanças...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analisando sua base financeira..."):
                response = answer_question(
                    user_input,
                    perfil,
                    summary,
                    context,
                    st.session_state.messages,
                )
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
```

## Dependências

```txt
streamlit>=1.36.0
pandas>=2.0.0
python-dotenv>=1.0.0
openai>=1.0.0
```

## Como executar

```bash
pip install -r requirements.txt
streamlit run src/app.py
```
