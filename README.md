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

## Informações técnicas (para o desenvolvedor)

- **Stack:** Hugo (gerador de site estático) + Decap CMS
- **Branch ativa:** `new_design`
- **Deploy:** GitHub Actions → GitHub Pages (ativado por push na branch `new_design`)
- **CMS:** Decap CMS com backend `git-gateway` via Netlify Identity
- **Netlify site:** `illustrious-moonbeam-ccac5a.netlify.app` (usado apenas para autenticação do CMS — o site público está no GitHub Pages)
- **Conteúdo:** pasta `content/` em formato Markdown
- **Estilos:** `static/css/main.css` (CSS puro, sem build step)
- **Imagens:** `img/` (acessível em `static/img` via symlink)

Para rodar o site localmente:
```bash
hugo server
```
Acesse em `http://localhost:1313`
