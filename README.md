# NEFIN — Site do Grupo de Pesquisa

Site oficial do NEFIN, disponível em **[nefin.com.br](https://nefin.com.br)**.

---

## Como editar o site

O site possui um painel de administração onde você pode editar o conteúdo sem precisar saber programação.

### 1. Acesse o painel

Abra o endereço abaixo no navegador e salve nos favoritos:

> **https://illustrious-moonbeam-ccac5a.netlify.app/admin/**

### 2. Faça login

Na tela de login, use o e-mail e a senha que você recebeu por e-mail ao ser convidado. Se ainda não recebeu um convite, peça ao responsável pelo site para te adicionar.

### 3. Edite o conteúdo

Após o login, você verá o painel com as seguintes seções:

| Seção | O que você pode fazer |
|---|---|
| **Faculty** | Adicionar, editar ou remover professores |
| **Researchers** | Adicionar, editar ou remover pesquisadores |
| **Students** | Adicionar, editar ou remover estudantes |
| **Alumni** | Adicionar, editar ou remover ex-alunos |
| **Published Papers** | Adicionar ou editar artigos publicados |
| **Working Papers** | Adicionar ou editar working papers |
| **Data Pages** | Editar as descrições e links de download dos datasets |

### 4. Salve as alterações

Após editar, clique em **"Publish"** (ou **"Save"** seguido de **"Publish"**). O site será atualizado automaticamente em cerca de **1 minuto**.

> Não é necessário fazer mais nada — o sistema cuida do resto sozinho.

---

## Como adicionar um novo editor

Para dar acesso ao painel a uma nova pessoa:

1. Acesse [app.netlify.com](https://app.netlify.com)
2. Entre no projeto **illustrious-moonbeam-ccac5a**
3. Vá em **Site configuration → Identity → Invite users**
4. Digite o e-mail da pessoa e clique em **Invite**

A pessoa receberá um e-mail com um link para criar a senha de acesso.

---

## Como o site funciona (visão geral)

O site é composto por três partes que trabalham juntas:

- **GitHub** — onde o código e o conteúdo do site ficam armazenados
- **Netlify** — onde o painel de edição fica hospedado
- **GitHub Pages** — onde o site público (`nefin.com.br`) fica hospedado

Quando alguém edita e publica pelo painel, o Netlify salva a alteração no GitHub, que por sua vez reconstrói e atualiza o site automaticamente.

---

## Quais arquivos são editáveis, e como viram o site publicado

O site não é feito de páginas HTML prontas — ele é **gerado automaticamente** a partir de arquivos-fonte. Entender essa diferença ajuda a saber onde mexer.

### O que é editável

| Onde | O que é | Como editar |
|---|---|---|
| `content/**/*.md` | Textos, nomes, links, tabelas — o conteúdo em si (professores, papers, datasets, etc.) | Pelo painel do CMS (recomendado) ou direto no arquivo `.md`, se você souber Git |
| `static/resources/**` | Os arquivos de dados de verdade (CSV, XLS, PDF) que os links de download apontam | Substituindo o arquivo direto no repositório (o CMS não faz upload desses arquivos) |
| `static/css/main.css` | A aparência visual do site (cores, espaçamento, layout) | Direto no arquivo, é CSS puro — não precisa compilar nada para ver o efeito localmente |
| `layouts/**` | Os "moldes" HTML que decidem onde cada campo do `.md` aparece na página | Direto no arquivo — exige conhecimento de Hugo/Go templates |
| `static/admin/config.yml` | Quais campos aparecem no painel do CMS para cada seção | Direto no arquivo — não é editável pelo próprio CMS |

Ou seja: **quem edita conteúdo do dia a dia só mexe em `content/` (via CMS) e, ocasionalmente, sobe um arquivo novo em `static/resources/`.** As pastas `layouts/`, `static/css/` e `static/admin/config.yml` são "código" do site e mudam raramente.

### Como isso é compilado

O site usa o **Hugo** (gerador de site estático). Rodar o comando abaixo lê tudo de `content/`, `layouts/` e `static/`, e junta em páginas HTML finais:

```bash
hugo --minify
```

Não existe passo de build para o CSS/JS — os arquivos em `static/` são copiados como estão. Só o Hugo "monta" as páginas, combinando o texto de cada `.md` com o molde correspondente em `layouts/`.

### Para onde vai o resultado compilado

O comando acima gera tudo dentro da pasta **`public/`**. Essa pasta:

- **não fica versionada no Git** (está no `.gitignore`) — é sempre recriada do zero a cada build;
- localmente, só aparece depois que você roda `hugo` ou `hugo server`;
- em produção, é gerada automaticamente pelo GitHub Actions (`.github/workflows/hugo.yml`) a cada push na branch `main`, e o conteúdo dessa pasta é o que fica publicado em **nefin.com.br** via GitHub Pages.

Resumindo o caminho de uma edição até o site no ar:

```
content/*.md (você edita)  ─┐
layouts/*.html             ─┼─▶  hugo --minify  ─▶  public/  ─▶  GitHub Pages (nefin.com.br)
static/**                  ─┘
```

---

## Informações técnicas (para o desenvolvedor)

- **Stack:** Hugo (gerador de site estático) + Decap CMS
- **Branch ativa:** `main`
- **Deploy:** GitHub Actions → GitHub Pages (ativado por push nas branches `main` e `new_design`; `main` é a que o CMS publica)
- **CMS:** Decap CMS com backend `git-gateway` via Netlify Identity, publicando direto na branch `main`
- **Netlify site:** `illustrious-moonbeam-ccac5a.netlify.app` (usado apenas para autenticação do CMS — o site público está no GitHub Pages)
- **Conteúdo:** pasta `content/` em formato Markdown
- **Estilos:** `static/css/main.css` (CSS puro, sem build step)
- **Imagens:** `img/` (acessível em `static/img` via symlink)

Para rodar o site localmente:
```bash
hugo server
```
Acesse em `http://localhost:1313`
