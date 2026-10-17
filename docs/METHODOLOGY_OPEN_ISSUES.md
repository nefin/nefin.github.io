# Pendências metodológicas

Levantamento de outubro de 2026, feito depois da atualização dos dados até 2026-09-08 pelo pipeline `nefin/python_risk_factors` (commit 9af63f7, PRs #3 a #17).

Compara o que o site publica com o PDF da metodologia (`static/nefindata/methodology/nefin_methodology.pdf`, de 14/09/2026). Nada aqui impede a publicação dos dados. Ao resolver um item, apague-o daqui.

## 1. Decisões de cálculo

### 1.1 Regra de exclusão por evento corporativo (seção 3)
A GOLL54 foi excluída depois da saída do Chapter 11. Sem a exclusão, o mercado dava +13,5% em 13/06/2025 e o SMB dava +166%. A exclusão é ad hoc, porque os critérios de elegibilidade não preveem tirar uma ação por evento corporativo.

**A decidir:** uma regra escrita para os próximos casos, por exemplo: "ações em recuperação judicial ou reestruturação são excluídas de … até …".

### 1.2 Taxa real de 1 ano no cost of equity (seção 7.2)
O PDF diz swap DI 360 dias deflacionado pelo IPCA esperado. O pipeline usa a LTN de 1 ano, porque o BCB parou de publicar o swap em 2019-09. O desvio é inevitável e está explicado na página do dataset, mas não no PDF.

## 2. O que o PDF precisa passar a dizer

| Seção | Hoje no PDF | O que publicamos |
|---|---|---|
| 5 (fatores) | Só pesos iguais, só diários | Duas ponderações (valor e iguais), nenhuma "oficial", em frequência diária e mensal. O fator mensal é a diferença dos retornos mensais das duas carteiras, como no Fama-French, e não o diário composto. |
| 7.1 (prêmio EUA) | Diz "monthly U.S. market risk premium" e depois "annual excess returns"; não cita a fonte | Retorno das ações sobre T-bill, do Ken French Data Library, composto em janelas de 1, 5, 10 e 20 anos |
| 7 (cost of equity) | Não diz se o resultado é real ou nominal | A fórmula soma taxa real + beta × prêmio, então o resultado seria real. Confirmar e dizer isso no PDF e na página. |
| 9.1 (dividend yield) | Série diária | O site publica uma observação por semana, no último pregão |
| 10.1 (short interest) | Razão Q/O, sem unidade | Em por mil (32 = 3,2%) |
| 10.2 (days-to-cover) | Em ações, ok | Em dias. A versão publicada até 2026-09 (~0,4) dividia ações por R$. |
| 10.3 (loan fee) | Só a média semanal, em fração | Também a diária (página Short Interest), em % ao ano. Falta dizer que cada ação entra uma vez por dia e que os picos de 2013–2014 são reais (arbitragem de JCP com VALE5/PETR4). |
| 4.8 (indústrias) | Lista os 7 setores | Falta a regra de classificação das empresas |
| Geral | Nenhuma data de início das séries | Fatores e carteiras desde 2001-01-02 (o pipeline começa em 2000; o site corta), iliquidez desde 2000-02, short interest desde 2012-11, loan fee desde 2013-01, cost of equity desde 2005-01 (construction desde 2009-02) |
| 8 (IVol-BR) | Descrita como série ativa | Descontinuada (exige dados de opções). A Spot Rate Curve, também arquivada, não aparece no PDF. |

## 3. Pontos a checar no pipeline

- **B/M anual (2.6 × 4.2).** A carteira do ano t é formada com o B/M de junho de t−1 (4.2), mas a aba anual "Average Book-to-Market" traz a média do B/M de junho de t dos membros. Pode ser intencional, mas o PDF não diz qual junho entra em cada uma.
- **Loan fee semanal × série antiga.** A série refeita a partir do diário tem correlação de 0,82 com a publicada até 2023, mas fica ~16% acima. Descobrir qual taxa do `base_btcer` (média, tomador ou doador) e qual universo reproduzem a série antiga, se alguém precisar da continuidade.
- **Dados que ficaram para o futuro:**
  - reativar a Spot Rate Curve (exigiria DI futuro);
  - reativar o IVol-BR (exigiria dados de opções).

## 4. Processo

- **Duas rotinas atualizando os fatores.** Em 28–29/09/2026 o `nefin_factors.csv` foi atualizado à mão, com a metodologia antiga (pico da GOLL incluído, SMB/HML sem a correção das seções 4.1–4.2). A atualização de outubro substituiu esse arquivo pela saída do pipeline. Da próxima vez, use só `python_general_scripts/import_from_pipeline.py`; senão as duas versões vão se sobrescrever.
- **Ideias do site ainda não feitas:**
  - página de mudanças (changelog) dos dados;
  - versões arquivadas e datadas dos arquivos, para reprodutibilidade;
  - atualização mensal automática (pipeline → importador → PR para revisão).
