# Base de Conhecimento

## Objetivo

A base fornece contexto financeiro estruturado para que o Finan responda com dados verificáveis, personalize a análise e admita quando uma informação não está disponível.

Os arquivos representam um cenário educacional adaptado para organização financeira pessoal. Eles não são consultados em bancos ou serviços externos.

## Arquivos Utilizados

| Arquivo | Formato | Uso |
|---|---|---|
| `perfil_investidor_luis_rosa.json` | JSON | Perfil, objetivos, mês de análise, metas e compromissos |
| `transacoes_luis_rosa.csv` | CSV | Entradas e saídas com data, descrição, categoria, valor e tipo |
| `historico_atendimento_luis_rosa.csv` | CSV | Dúvidas anteriores e continuidade do atendimento |
| `produtos_financeiros_luis_rosa.json` | JSON | Opções financeiras e regras de adequação ao momento do usuário |

## Estrutura

```text
data/
|-- historico_atendimento_luis_rosa.csv
|-- perfil_investidor_luis_rosa.json
|-- produtos_financeiros_luis_rosa.json
`-- transacoes_luis_rosa.csv
```

## Processamento

Ao iniciar, a aplicação:

1. Localiza a pasta `data`.
2. Carrega os arquivos JSON com codificação UTF-8.
3. Carrega os arquivos CSV e normaliza os nomes das colunas.
4. Converte valores monetários para números.
5. Converte a coluna de data.
6. Filtra as transações pelo campo `mes_analise` do perfil.
7. Calcula entradas, saídas, saldo, cartão e categorias.
8. Monta um contexto textual para a LLM.

Para junho de 2026, a base resulta em:

- Entradas: **R$ 7.064,52**
- Saídas: **R$ 9.511,45**
- Saldo previsto: **-R$ 2.446,93**
- Diagnóstico: **Atenção: mês negativo**

## Estratégias de Qualidade

- Campos desconhecidos, como patrimônio total e reserva atual, permanecem `null`.
- A LLM recebe valores calculados pelo código, não precisa somá-los por conta própria.
- O mês analisado é explícito para evitar misturar transações futuras.
- O histórico enviado ao modelo é limitado às interações mais recentes.
- Os produtos financeiros incluem indicação de risco e momento adequado.

## Atualização da Base

Para atualizar o cenário:

1. Inclua ou altere registros nos arquivos da pasta `data`.
2. Mantenha as colunas `data`, `descricao`, `categoria`, `valor` e `tipo` no CSV de transações.
3. Atualize `indicadores_mes_atual.mes_analise` no perfil.
4. Reinicie ou recarregue a aplicação.

## Privacidade

O uso do Ollama permite que o contexto seja processado localmente. Ainda assim, antes de publicar um projeto real, dados pessoais e financeiros devem ser anonimizados ou substituídos por dados fictícios.
