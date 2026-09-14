---
title: "CAPM in Python: Estimating Small-Cap Beta with NEFIN Data"
title_pt: "CAPM em Python: Estimando o Beta do Small Cap com Dados do NEFIN"
date: 2026-09-14
language: "en"
bilingual: true
math: true
author: "Kauê Lopes de Moraes"
author_affiliation: "Ph.D Candidate, University of São Paulo"
author_url: ""
author_photo: ""
author_bio: "Ph.D. candidate in Economics at FEA-USP, advised by Rodrigo De Losso. Works on NEFIN's data infrastructure, including the Python library introduced in this post."
author_bio_pt: "Doutorando em Economia na FEA-USP, orientado por Rodrigo De Losso. Trabalha na infraestrutura de dados do NEFIN, incluindo a biblioteca Python apresentada neste texto."
summary: "How much market risk does a small-cap portfolio really carry? A classic CAPM exercise on real NEFIN data, worked out in a few lines of Python."
summary_pt: "Quanto de risco de mercado um portfólio small-cap realmente carrega? Um exercício clássico de CAPM com dados reais do NEFIN, resolvido em poucas linhas de Python."
image: "/img/insights/capm-small-cap-beta-og.png"
topics: ["Python", "Data"]
---

{{% lang-en %}}
How much market risk does a small-cap portfolio actually carry, compared to the market
as a whole? It's one of the oldest questions in asset pricing, and a good excuse to work
through it end to end on real Brazilian data.

> This post is a **teaching exercise**, not investment advice or a research finding. It
> demonstrates one standard technique — the CAPM market-model regression — on real,
> full-sample NEFIN data, with no cherry-picking of dates. But a two-portfolio comparison
> over one historical sample proves nothing about future risk premia, and it isn't how
> NEFIN's factors are actually used in serious asset-pricing work — that requires a lot
> more care than five lines of code.

The market model behind the CAPM says a portfolio's excess return should mostly be a
scaled version of the market's excess return:

{{< math display="true" >}}R_p - R_f = \alpha + \beta \,(R_m - R_f) + \varepsilon{{< /math >}}

β measures how much market risk the portfolio carries (β = 1 means "moves like the
market"); α is whatever's left over once market risk is accounted for — CAPM says it
should average out to zero. Textbooks usually estimate this for a single stock; here we
use one of NEFIN's own size-sorted portfolios instead, since NEFIN already built it for
us.

This particular equation has been sitting in every finance textbook since the 1960s, but
it didn't start as a formula — it started as a question Harry Markowitz had already
half-answered. His 1952 portfolio theory showed investors how to trade off risk against
return once they *have* a set of possible portfolios to choose from, but it never said
where the returns and risks themselves come from. Sharpe (1964), and independently
Lintner (1965) and Mossin (1966), worked out what has to be true in equilibrium if every
investor behaves that way: only the portion of risk that can't be diversified away — the
part tied to the whole market — should carry a reward. Everything else averages out.
Sharpe shared the 1990 Nobel with Markowitz for it.

The model is elegant partly because it's so exposed: it makes one clean, testable claim,
and researchers spent the following decades testing it hard. Richard Roll pointed out in
1977 that you can't really test CAPM at all, since nobody observes the *true* market
portfolio — NEFIN's index, like any other, is a proxy. And in 1992, Fama and French found
that size and book-to-market predicted returns well beyond what beta alone could explain,
which is exactly the empirical gap that multifactor models — including the SMB and HML
factors NEFIN computes — were built to close. The exercise below still uses the original,
simplest version on purpose: it's the baseline everything since has been measured
against.

```python
import nefin as nd
import statsmodels.api as sm

factors = nd.load_risk_factors()
portfolios = nd.load_portfolios(sort_by="size", n=3)

df = factors.join(portfolios, how="inner")
df["excess_small"] = df["size_1"] - df["risk_free"]   # size_1 = smallest-firm portfolio

model = sm.OLS(df["excess_small"], sm.add_constant(df["rm_minus_rf"])).fit()
print(model.params)
print(f"R-squared: {model.rsquared:.2f}")
```

Running this on the full sample — 2001 to 2023, 5,615 trading days — gives:

- **β = 0.87** — the small-cap portfolio moves *less* than one-for-one with the market
- **α ≈ −0.55% per year** — statistically indistinguishable from zero (t ≈ −0.16),
  consistent with what CAPM predicts
- **R² = 0.65** — the market factor explains 65% of this portfolio's day-to-day
  variation

<img src="/img/insights/capm-small-cap-beta-en.png" alt="Scatter plot of the small-cap portfolio's daily excess return against the market factor's daily excess return, with a fitted regression line of slope 0.87">

The more interesting number here isn't β — it's R². Run the exact same regression on
NEFIN's large-cap portfolio instead (swap `size_1` for `size_3`) and β comes out at 0.95,
with R² jumping to 0.93. That 0.65-vs-0.93 gap is the textbook illustration of
*idiosyncratic risk*: small,
less-liquid firms carry return variation that one market factor alone doesn't capture —
part of it diversifiable, part of it exactly what NEFIN's own SMB factor exists to
price. If you want a next step to try yourself, that comparison — or adding SMB, HML and
WML as extra regressors — is two more lines of `nefin` code away.

## What the beta might be telling us

There's a detail worth sitting with: the small-cap portfolio's beta (0.87) is *lower*
than the large-cap portfolio's (0.95), not higher. That can feel backwards — smaller,
less-established firms are usually described as riskier, so a beta below one, and below
large caps', looks like the opposite of what most people expect.

One standard explanation doesn't require small caps to be genuinely calmer, only
harder to price every single day. Many smaller Brazilian stocks trade less frequently
than the large, liquid names driving the index, so a chunk of their "daily" return is
really yesterday's price catching up today — their measured co-movement with the market
gets diluted simply because some of their price reaction is delayed by a day or more.
This is an old, well-documented issue (Scholes and Williams, 1977; Dimson, 1979), and the
standard fix is to regress on lagged and lead market returns too, not just today's —
something a five-line teaching regression skips on purpose. It's also consistent with
the lower R² we found earlier: some of what looks like "idiosyncratic" variation in the
small-cap portfolio may really be market risk showing up a day late, not risk that's
genuinely uncorrelated with the market. None of this changes the numbers above — it's a
reminder that a clean estimate and a *correctly interpreted* one aren't always the same
thing, and it's exactly the kind of question that turns a five-line regression into a
real research project.

## A side benefit: reproducibility

A script that downloads NEFIN data by hand usually ends up saving a local copy of the
CSV — and that copy starts going stale on day one. Six months later, nobody remembers
whether it still reflects the latest series. Calling `nd.load_risk_factors()` instead
flips the default: every run already fetches the current version, and freezing a
specific snapshot for a paper becomes an explicit decision instead of an accident.

## About the data

Everything above came from `nefin`, a small Python client for NEFIN's public datasets —
risk factors, portfolios, cost of equity, the spot rate curve, short interest, and more.

```bash
pip install nefin
# the portfolios call above needs the optional Excel extra:
pip install "nefin[excel]"
```

The rest of the catalog works the same way — `nd.load_cost_of_equity()`,
`nd.load_spot_rate_curve()`, `nd.load_short_interest()` — and all of it is also
downloadable directly from [nefin.com.br/data](/data/) if you'd rather skip Python
entirely.
{{% /lang-en %}}

{{% lang-pt %}}
Quanto de risco de mercado um portfólio small-cap realmente carrega, comparado ao
mercado como um todo? É uma das perguntas mais antigas de asset pricing — e uma boa
desculpa pra resolver ela de ponta a ponta em dados brasileiros de verdade.

> Este texto é um **exercício didático**, não recomendação de investimento nem
> resultado de pesquisa. Ele demonstra uma técnica padrão — a regressão do modelo de
> mercado do CAPM — em dados reais e completos do NEFIN, sem seleção de datas. Mas uma
> comparação entre dois portfólios ao longo de uma única amostra histórica não prova
> nada sobre prêmios de risco futuros, e não é assim que os fatores do NEFIN são
> efetivamente usados em trabalho sério de asset pricing — isso exige bem mais cuidado
> do que cinco linhas de código.

O modelo de mercado por trás do CAPM diz que o retorno excedente de um portfólio deve
ser, em boa parte, uma versão escalada do retorno excedente do mercado:

{{< math display="true" >}}R_p - R_f = \alpha + \beta \,(R_m - R_f) + \varepsilon{{< /math >}}

β mede quanto risco de mercado o portfólio carrega (β = 1 significa "se move junto com o
mercado"); α é o que sobra depois de descontar esse risco de mercado — o CAPM diz que
deveria, em média, ser zero. Livros-texto costumam estimar isso para uma ação só; aqui
usamos um dos próprios portfólios do NEFIN ordenados por tamanho, já que o NEFIN já o
montou pra gente.

Essa equação está em todo livro-texto de finanças desde os anos 1960, mas ela não
começou como fórmula — começou como uma pergunta que Harry Markowitz já tinha respondido
pela metade. A teoria de portfólio de 1952 dele mostrava ao investidor como pesar risco
contra retorno uma vez que ele *já tem* um conjunto de portfólios possíveis pra escolher,
mas nunca dizia de onde vinham esses retornos e riscos. Sharpe (1964), e
independentemente Lintner (1965) e Mossin (1966), resolveram o que precisa ser verdade em
equilíbrio se todo investidor se comportar assim: só a parcela de risco que não dá pra
diversificar — a parte ligada ao mercado como um todo — deveria ser recompensada. O resto
se cancela. Sharpe dividiu o Nobel de 1990 com Markowitz por causa disso.

O modelo é elegante justamente por ser tão exposto: faz uma afirmação limpa e testável, e
os pesquisadores passaram as décadas seguintes testando ela a fundo. Richard Roll
apontou em 1977 que não dá pra testar o CAPM de verdade, já que ninguém observa o
portfólio de mercado *verdadeiro* — o índice do NEFIN, como qualquer outro, é uma proxy.
E em 1992, Fama e French encontraram que tamanho e book-to-market previam retornos bem
além do que o beta sozinho explicava — exatamente o buraco empírico que os modelos
multifatoriais, incluindo os próprios fatores SMB e HML que o NEFIN calcula, foram
construídos pra fechar. O exercício abaixo usa de propósito a versão original, mais
simples: é a referência contra a qual tudo depois foi medido.

```python
import nefin as nd
import statsmodels.api as sm

factors = nd.load_risk_factors()
portfolios = nd.load_portfolios(sort_by="size", n=3)

df = factors.join(portfolios, how="inner")
df["excess_small"] = df["size_1"] - df["risk_free"]   # size_1 = portfólio das menores firmas

model = sm.OLS(df["excess_small"], sm.add_constant(df["rm_minus_rf"])).fit()
print(model.params)
print(f"R-squared: {model.rsquared:.2f}")
```

Rodando isso na amostra completa — 2001 a 2023, 5.615 pregões — dá:

- **β = 0,87** — o portfólio small-cap se move *menos* do que um-para-um com o mercado
- **α ≈ −0,55% ao ano** — estatisticamente indistinguível de zero (t ≈ −0,16),
  consistente com o que o CAPM prevê
- **R² = 0,65** — o fator de mercado explica 65% da variação diária desse portfólio

<img src="/img/insights/capm-small-cap-beta-pt.png" alt="Gráfico de dispersão do retorno excedente diário do portfólio small-cap contra o retorno excedente diário do fator de mercado, com reta de regressão ajustada de inclinação 0,87">

O número mais interessante aqui não é o β — é o R². Rode exatamente a mesma regressão no
portfólio large-cap do NEFIN (troque `size_1` por `size_3`) e o β sai em 0,95, com o R²
subindo para 0,93. Essa diferença entre 0,65 e 0,93 é a ilustração clássica de *risco
idiossincrático*: firmas pequenas e menos líquidas carregam variação de retorno que um
único fator de mercado não captura sozinho — parte diversificável, parte exatamente o que
o próprio fator SMB do NEFIN existe para precificar. Se você quiser um próximo passo pra
tentar por conta própria, essa comparação — ou adicionar SMB, HML e WML como regressores
extras — está a duas linhas de código de `nefin` de distância.

## O que o beta talvez esteja nos dizendo

Tem um detalhe que vale a pena examinar: o beta do portfólio small-cap (0,87) é *menor*
que o do large-cap (0,95), não maior. Isso pode parecer invertido — firmas menores e
menos estabelecidas costumam ser descritas como mais arriscadas, então um beta abaixo de
um, e abaixo do das large caps, parece o oposto do que a maioria esperaria.

Uma explicação padrão não exige que as small caps sejam genuinamente mais calmas, só que
sejam mais difíceis de precificar todo santo dia. Muitas ações brasileiras menores
negociam com menos frequência do que os papéis grandes e líquidos que puxam o índice,
então parte do retorno "diário" delas é, na verdade, o preço de ontem ainda se ajustando
hoje — a covariância medida com o mercado acaba diluída simplesmente porque parte da
reação de preço chega atrasada em um dia ou mais. Esse é um problema antigo e bem
documentado (Scholes e Williams, 1977; Dimson, 1979), e o ajuste padrão é regredir também
contra o retorno de mercado defasado e adiantado, não só o de hoje — algo que uma
regressão didática de cinco linhas pula de propósito. Isso também é consistente com o R²
menor que encontramos antes: parte do que parece variação "idiossincrática" no portfólio
small-cap pode, na verdade, ser risco de mercado aparecendo um dia atrasado, não risco
genuinamente descorrelacionado do mercado. Nada disso muda os números acima — é só um
lembrete de que uma estimativa limpa e uma estimativa *corretamente interpretada* nem
sempre são a mesma coisa, e é exatamente o tipo de pergunta que transforma uma regressão
de cinco linhas em um projeto de pesquisa de verdade.

## Um efeito colateral bom: reprodutibilidade

Um script que baixa dados do NEFIN na mão costuma acabar salvando uma cópia local do
CSV — e essa cópia começa a envelhecer no primeiro dia. Seis meses depois, ninguém lembra
se ela ainda reflete a série mais recente. Chamar `nd.load_risk_factors()` em vez disso
inverte o padrão: toda execução já busca a versão atual, e congelar uma versão específica
para um artigo vira uma decisão explícita, não um esquecimento.

## Sobre os dados

Tudo acima veio do `nefin`, um cliente Python leve para as bases públicas do NEFIN —
fatores de risco, portfólios, custo de capital, curva de juros, aluguel de ações e mais.

```bash
pip install nefin
# o load_portfolios usado acima precisa do extra opcional de Excel:
pip install "nefin[excel]"
```

O resto do catálogo funciona do mesmo jeito — `nd.load_cost_of_equity()`,
`nd.load_spot_rate_curve()`, `nd.load_short_interest()` — e tudo também pode ser baixado
direto em [nefin.com.br/data](/data/), sem precisar de Python.
{{% /lang-pt %}}
