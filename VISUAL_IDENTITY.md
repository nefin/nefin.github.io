# NEFIN — Identidade Visual

Documento de referência para decisões de design do site. Registra o que existia no site antigo e o que foi adotado no redesign.

---

## Site Antigo (Bootstrap / Enlight Theme)

### Cores

| Variável | Hex | Papel |
|---|---|---|
| `$brand-primary` | `#6a41ed` | Cor principal — roxo/violeta usado em CTAs, destaques, navbar ativa |
| `$brand-secondary` | `#49D292` | Cor secundária — verde menta usada em dropdowns e acentos |
| `$brand-black` | `#000000` | Texto escuro |
| `$brand-white` | `#ffffff` | Fundos brancos |
| — | `#181920` | Fundo do footer (quase preto) |
| — | `#EFF0F4` | Fundo de seções alternadas (cinza muito claro) |
| — | `#8b8e94` | Texto secundário / muted |
| — | `#dddde0` | Bordas e separadores |

> As cores de redes sociais (`#3b5998` Facebook, `#1da1f2` Twitter etc.) eram apenas ícones — não fazem parte da identidade do NEFIN.

### Tipografia

| Papel | Fonte | Peso |
|---|---|---|
| Títulos e UI | **Raleway** (Google Fonts) | 300, 400, 500, 700 |
| Corpo de texto | **Open Sans** (Google Fonts) | 400 |

### Observações sobre o site antigo

- Paleta **roxo + verde** sem relação direta com a identidade da USP ou da área de finanças
- Fontes modernas e geométricas (Raleway), adequadas mas sem caráter acadêmico
- Layout baseado no tema genérico "Enlight" da ProBootstrap — não era design próprio
- Ausência de hierarquia clara entre seções

---

## Site Novo (Hugo — em produção)

### Cores

| Variável CSS | Hex | Papel |
|---|---|---|
| `--primary` | `#1B3A6B` | Azul navy — cor principal, navbar, hero, headers |
| `--primary-dark` | `#0f2444` | Azul mais escuro — footer |
| `--primary-light` | `#2a52a0` | Azul mais claro — hover states |
| `--accent` | `#C8963E` | Dourado — acentos, hovers, bordas ativas, badges |
| `--white` | `#ffffff` | Fundo principal |
| `--gray-50` | `#f9fafb` | Fundo de seções alternadas |
| `--gray-100` | `#f3f4f6` | Superfícies internas |
| `--gray-200` | `#e5e7eb` | Bordas |
| `--gray-500` | `#6b7280` | Texto secundário / muted |
| `--gray-700` | `#374151` | Texto de navegação |
| `--gray-900` | `#111827` | Texto principal |

### Tipografia

| Papel | Fonte | Fonte de carga |
|---|---|---|
| Títulos (h1–h4) | **Georgia**, Times New Roman, serif | Sistema — sem Google Fonts |
| Corpo, UI, navegação | **System UI** (-apple-system, Segoe UI, Roboto…) | Sistema — sem Google Fonts |

> A escolha por fontes do sistema elimina dependência de carregamento externo, melhora performance e privacidade.

### Princípios de design adotados

- **Acadêmico e sóbrio** — inspirado em sites de grupos de pesquisa de referência (Princeton, LSE Economics)
- **Hierarquia por tipografia** — serifado para títulos, sans para corpo
- **Azul navy** remete à USP e transmite credibilidade institucional
- **Dourado** como acento elegante, sem exagero
- **Espaço em branco generoso** — conteúdo respira, fácil de ler
- **Sem fontes externas** — carregamento mais rápido, sem rastreadores do Google Fonts

---

## Decisões pendentes

- [ ] Definir se o logotipo "NEFIN" na navbar fica só em texto ou ganha um símbolo
- [ ] Avaliar se inclui foto da USP / FEA no hero ou mantém fundo sólido
- [ ] Decidir o tom exato do dourado — pode ser ajustado de `#C8963E` para algo mais frio ou mais vivo
- [ ] Avaliar se a cor primária se aproxima mais do azul USP oficial (`#003082`)

---

## Referência de cores USP

Para decisões futuras que queiram alinhar com a identidade da universidade:

| Cor | Hex |
|---|---|
| Azul USP (oficial) | `#003082` |
| Azul USP claro | `#0066CC` |
| Amarelo USP | `#F5A800` |
