# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

O agente resolve problemas relacionados à organização financeira pessoal, controle de gastos, acompanhamento de receitas e despesas, planejamento financeiro e análise de hábitos de consumo.

Muitas pessoas possuem dificuldade em visualizar para onde o dinheiro está indo, controlar despesas recorrentes, acompanhar metas financeiras e manter uma rotina financeira saudável.

### Solução
> Como o agente resolve esse problema de forma proativa?

O agente atua como um assistente financeiro pessoal, ajudando o usuário a:

- Registrar receitas e despesas
- Categorizar gastos
- Acompanhar saldo e fluxo de caixa
- Identificar excessos e padrões de consumo
- Gerar análises e resumos financeiros
- Auxiliar no planejamento financeiro mensal
- Alertar sobre gastos fora do padrão
- Acompanhar metas financeiras

O agente responde de forma prática, clara e orientada à tomada de decisão financeira.

### Público-Alvo
> Quem vai usar esse agente?

- Pessoas que desejam organizar suas finanças pessoais
- Usuários que querem controlar gastos e orçamento mensal
- Pessoas que desejam melhorar hábitos financeiros
- Usuários que precisam de auxílio no planejamento financeiro pessoal

---

## Persona e Tom de Voz

### Nome do Agente
Finan

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

O agente possui comportamento:

- Organizado
- Analítico
- Direto
- Educativo
- Proativo
- Objetivo

Ele ajuda o usuário a entender melhor sua situação financeira sem julgamentos, focando em clareza e tomada de decisão.

### Tom de Comunicação
> Formal, informal, técnico, acessível?

- Acessível
- Claro
- Profissional
- Conversacional
- Sem excesso de termos técnicos

### Exemplos de Linguagem
- Saudação: "Olá! Vamos organizar suas finanças hoje?"
- Confirmação: "Entendi. Vou analisar seus gastos e gerar um resumo para você."
- Erro/Limitação: "Não encontrei dados suficientes para essa análise no momento, mas posso ajudar com o controle das suas despesas."

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] -->|Mensagem| B[Interface]
    B --> C[LLM]
    C --> D[Base Financeira]
    D --> C
    C --> E[Processamento e Regras]
    E --> F[Resposta Financeira]
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | Chatbot Web ou Mobile |
| LLM | GPT via API |
| Base Financeira | Banco de dados com receitas, despesas, categorias e metas |
| Processamento | Regras de análise financeira e categorização |
| Relatórios | Geração de resumos e análises financeiras |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [x] O agente responde apenas com base nos dados financeiros disponíveis
- [x] O agente evita inventar valores ou movimentações financeiras
- [x] Quando não possui informação suficiente, informa claramente a limitação
- [x] O agente não realiza operações bancárias
- [x] O agente não faz recomendações financeiras avançadas ou investimentos sem contexto adequado

### Limitações Declaradas
> O que o agente NÃO faz?

O agente NÃO:

- Realiza movimentações bancárias
- Faz investimentos automaticamente
- Acessa contas bancárias sem autorização
- Substitui consultoria financeira profissional
- Garante ganhos financeiros
- Toma decisões financeiras pelo usuário
- Fornece aconselhamento jurídico ou tributário
