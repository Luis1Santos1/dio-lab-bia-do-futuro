# Pitch Final - Finan

## Narração para o ElevenLabs

Use somente o texto deste bloco no ElevenLabs.

```text
Muitas pessoas registram receitas e despesas em planilhas, mas ainda têm dificuldade para transformar esses números em decisões práticas.

Elas não sabem com clareza para onde o dinheiro está indo, quanto o cartão está comprometendo o orçamento, se o mês vai terminar positivo ou se realmente existe dinheiro disponível para uma nova compra ou investimento.

Para ajudar nesse problema, eu desenvolvi o Finan, um assistente financeiro pessoal com inteligência artificial.

O Finan transforma uma base financeira organizada em uma experiência simples de análise e conversa.

A aplicação carrega arquivos locais com o perfil do usuário, suas transações, metas, compromissos, histórico de atendimento e produtos financeiros disponíveis.

O sistema utiliza Python e Pandas para calcular os indicadores de forma confiável. A inteligência artificial recebe esses resultados já processados, reduzindo o risco de erros e respostas inventadas.

Na tela principal, podemos visualizar o resumo de junho de 2026.

O usuário possui sete mil e sessenta e quatro reais e cinquenta e dois centavos em entradas, nove mil quinhentos e onze reais e quarenta e cinco centavos em saídas e um saldo previsto negativo de dois mil quatrocentos e quarenta e seis reais e noventa e três centavos.

O gráfico também mostra as categorias que mais pressionam o orçamento, como cartão de crédito, transporte, moradia e compras.

Além do dashboard, o usuário pode conversar com o agente.

Ao perguntar como está sua situação financeira, o Finan apresenta os valores encontrados, destaca o saldo negativo e recomenda ações práticas, como controlar o cartão, evitar novas parcelas e revisar contas pendentes.

Quando perguntamos onde o usuário está gastando mais, o agente utiliza as categorias calculadas diretamente da base.

E se perguntarmos se é um bom momento para investir, o Finan prioriza primeiro o equilíbrio do orçamento e a formação de uma reserva de emergência.

O agente também possui regras de segurança. Ele não inventa informações ausentes, não solicita senhas, não realiza operações bancárias e informa quando uma pergunta está fora do seu escopo.

Como diferencial, o projeto utiliza o Ollama com o modelo gpt-oss executado localmente. Isso reduz a dependência de serviços pagos e permite que os dados permaneçam no computador do usuário.

O projeto também possui respostas locais para análises essenciais, garantindo rapidez mesmo quando o modelo de inteligência artificial exigir mais processamento.

O Finan demonstra como inteligência artificial, dados estruturados e regras de segurança podem tornar a organização financeira mais clara, acessível e orientada à ação.

Esse é o Finan: dados financeiros transformados em decisões mais conscientes.
```

## Plano de Gravação

### 0:00 - 0:28 | O problema

**Narração:** do início até “nova compra ou investimento”.

**Ação no vídeo:**

1. Comece com a aplicação aberta.
2. Mostre rapidamente o dashboard inteiro.
3. Faça um movimento lento destacando os indicadores e o gráfico.

**Não digite nenhuma pergunta ainda.**

---

### 0:28 - 0:58 | Apresentação da solução

**Narração:** de “Para ajudar nesse problema” até “respostas inventadas”.

**Ação no vídeo:**

1. Mostre o título e a descrição do aplicativo.
2. Destaque a sidebar com os quatro arquivos carregados.
3. Mostre `Provedor: ollama` e `Modelo: gpt-oss`.
4. Abra o campo “Ver contexto resumido enviado ao agente”.
5. Role lentamente pelo contexto e feche o campo.

---

### 0:58 - 1:28 | Dashboard

**Narração:** de “Na tela principal” até “moradia e compras”.

**Ação no vídeo:**

1. Mostre o período analisado: junho de 2026.
2. Passe pelos indicadores:
   - Entradas: R$ 7.064,52
   - Saídas: R$ 9.511,45
   - Saldo previsto: -R$ 2.446,93
3. Destaque o diagnóstico de mês negativo.
4. Mostre as maiores barras do gráfico.

---

### 1:28 - 1:58 | Primeira demonstração

**Narração:** de “Além do dashboard” até “revisar contas pendentes”.

**Prompt para enviar:**

```text
Como está minha situação financeira esse mês?
```

**Ação no vídeo:**

1. Digite ou selecione a pergunta.
2. Envie.
3. Role lentamente pela resposta.
4. Destaque entradas, saídas, saldo negativo e próximas ações.

---

### 1:58 - 2:16 | Categorias de gastos

**Narração:** de “Quando perguntamos” até “diretamente da base”.

**Prompt para enviar:**

```text
Onde estou gastando mais?
```

**Ação no vídeo:**

1. Envie a pergunta.
2. Mostre a lista de maiores categorias.
3. Relacione visualmente a resposta com o gráfico do dashboard.

---

### 2:16 - 2:32 | Decisão sobre investimentos

**Narração:** de “E se perguntarmos” até “reserva de emergência”.

**Prompt para enviar:**

```text
Posso investir esse mês?
```

**Ação no vídeo:**

1. Envie a pergunta.
2. Mostre o saldo negativo apresentado na resposta.
3. Destaque a recomendação de organizar o orçamento antes de investir.

---

### 2:32 - 2:48 | Segurança

**Narração:** de “O agente também possui” até “fora do seu escopo”.

**Prompt para enviar:**

```text
Qual é meu patrimônio total?
```

**Ação no vídeo:**

1. Envie a pergunta.
2. Mostre que o agente não inventa o patrimônio.

**Prompt alternativo, caso haja tempo:**

```text
Qual a previsão do tempo para amanhã?
```

Mostre que o agente informa que a pergunta está fora do escopo financeiro.

---

### 2:48 - 3:00 | Diferencial e encerramento

**Narração:** de “Como diferencial” até o final.

**Ação no vídeo:**

1. Volte ao topo da aplicação.
2. Mostre novamente `ollama` e `gpt-oss` na sidebar.
3. Termine com o dashboard completo na tela.
4. Faça uma pausa de dois segundos após a última frase.

## Configuração Sugerida no ElevenLabs

- Idioma: português do Brasil
- Voz: profissional, natural e consultiva
- Velocidade: entre `0.95` e `1.0`
- Estabilidade: média ou alta
- Expressividade: moderada
- Evite música alta durante a narração

## Checklist Antes de Gravar

- [ ] Aplicação aberta em `http://localhost:8501`
- [ ] Dashboard exibindo junho de 2026
- [ ] Ollama e `gpt-oss` visíveis na sidebar
- [ ] Zoom do navegador entre 90% e 100%
- [ ] Notificações do Windows desativadas
- [ ] Perguntas copiadas para facilitar a gravação
- [ ] Captura em 1080p
- [ ] Narração com duração máxima de 3 minutos
- [ ] Link do vídeo adicionado abaixo

## Link do Vídeo

[Assistir ou baixar o pitch do Finan](https://github.com/Luis1Santos1/dio-lab-bia-do-futuro/releases/download/v1.0.0/finan-pitch.mp4)

[Ver a release completa](https://github.com/Luis1Santos1/dio-lab-bia-do-futuro/releases/tag/v1.0.0)
