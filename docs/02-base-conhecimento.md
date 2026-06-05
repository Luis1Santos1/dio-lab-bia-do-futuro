# Base de Conhecimento

## Dados Utilizados

A base de conhecimento do agente foi construída a partir dos arquivos da pasta `data`, ajustados com base na planilha real de controle financeiro do Luis Rosa.

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento_luis_rosa.csv` | CSV | Contextualizar interações anteriores, preferências, objetivos financeiros e dúvidas recorrentes do usuário |
| `perfil_investidor_luis_rosa.json` | JSON | Personalizar análises financeiras com base no perfil, renda, metas, compromissos e situação atual |
| `produtos_financeiros_luis_rosa.json` | JSON | Apoiar recomendações financeiras compatíveis com o momento do usuário, priorizando organização, segurança e fluxo de caixa |
| `transacoes_luis_rosa.csv` | CSV | Analisar entradas, contas fixas, despesas variáveis, cartão de crédito, categorias de gasto e evolução mensal |

> [!TIP]
> A base foi adaptada para representar um cenário financeiro pessoal realista, focado em controle de orçamento, organização de despesas, acompanhamento de metas e apoio à tomada de decisão financeira.

---

## Adaptações nos Dados

Os arquivos mockados originais foram modificados para refletir o caso real do Luis Rosa, utilizando como referência a planilha `CONTROLE FINANÇAS - LUIS ROSA`.

As principais adaptações realizadas foram:

- Substituição do perfil fictício por um perfil financeiro personalizado do Luis Rosa.
- Inclusão de renda mensal prevista, compromissos financeiros, metas e diagnóstico financeiro.
- Geração de transações com base nas abas da planilha, como:
  - Contas a receber;
  - Contas a pagar;
  - Descritivo dos cartões;
  - Metas;
  - Premissas financeiras;
  - Dívidas e cenários.
- Ajuste dos produtos financeiros para um contexto mais conservador e coerente com o momento atual do usuário.
- Priorização de recomendações voltadas para:
  - Controle de fluxo de caixa;
  - Redução de gastos com cartão;
  - Organização de contas fixas;
  - Construção de reserva financeira;
  - Evitar novos compromissos antes de estabilizar o orçamento.
- Campos sem informação clara na planilha, como idade, patrimônio total e reserva atual, foram mantidos como `null` para evitar inferências incorretas.

---

## Estratégia de Integração

### Como os dados são carregados?

Os arquivos CSV e JSON são carregados a partir da pasta `data` no início da execução do agente.

Os arquivos JSON são utilizados para recuperar informações estruturadas sobre o perfil financeiro do usuário e os produtos financeiros disponíveis.

Os arquivos CSV são utilizados para leitura tabular das transações e histórico de atendimento, permitindo análises por data, categoria, tipo de movimentação, descrição e valor.

Exemplo de carregamento esperado:

```text
/data
├── historico_atendimento_luis_rosa.csv
├── perfil_investidor_luis_rosa.json
├── produtos_financeiros_luis_rosa.json
└── transacoes_luis_rosa.csv
