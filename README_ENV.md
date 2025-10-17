# 🔐 Configuração de Variáveis de Ambiente

## 📋 Por que usar .env?

As credenciais de email (usuário e senha) são dados **sensíveis** e não devem ser versionadas no Git. Por isso, usamos um arquivo `.env` que é **ignorado** pelo Git.

---

## 🚀 Configuração Inicial

### 1. Copiar o arquivo de exemplo

```bash
cp .env.example .env
```

### 2. Editar o arquivo .env

Abra o arquivo `.env` e preencha com suas credenciais:

```env
# Configurações de Email SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_SSL=false

# Suas credenciais
SMTP_USERNAME=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_app_aqui
```

---

## 🔑 Como obter Senha de App do Gmail

1. **Ativar Verificação em 2 Etapas:**
   - Acesse: https://myaccount.google.com/security
   - Ative a "Verificação em duas etapas"

2. **Gerar Senha de App:**
   - Acesse: https://myaccount.google.com/apppasswords
   - Selecione "App: Email"
   - Selecione "Dispositivo: Windows"
   - Clique em "Gerar"
   - Copie a senha (formato: `xxxx xxxx xxxx xxxx`)

3. **Usar a senha no .env:**
   ```env
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx
   ```

---

## 📁 Estrutura de Arquivos

```
sender_xml_new_version/
├── .env                 # ❌ Não versionar (ignorado pelo Git)
├── .env.example         # ✅ Versionar (template)
├── .gitignore           # ✅ Versionar (ignora .env)
├── config/
│   └── settings.json    # ⚠️ Sem credenciais sensíveis
└── modules/
    └── env_config.py    # ✅ Gerenciador de variáveis
```

---

## ⚙️ Como Funciona

### Ordem de Prioridade

1. **Variáveis do .env** (maior prioridade)
2. **Variáveis de ambiente do sistema**
3. **Valores padrão no código**

### Código

```python
from modules.env_config import EnvConfig

env = EnvConfig()
smtp_config = env.get_smtp_config()

# smtp_config contém:
# {
#     'server': 'smtp.gmail.com',
#     'port': 587,
#     'username': 'seu_email@gmail.com',
#     'password': 'sua_senha_app',
#     'use_ssl': False
# }
```

---

## ✅ Boas Práticas

### ✔️ Fazer:
- ✅ Copiar `.env.example` para `.env`
- ✅ Adicionar `.env` no `.gitignore`
- ✅ Documentar variáveis no `.env.example`
- ✅ Usar senhas de app (não a senha real)

### ❌ Não Fazer:
- ❌ Commitar arquivo `.env`
- ❌ Compartilhar senhas em código
- ❌ Hardcodear credenciais
- ❌ Usar senha real do email

---

## 🔒 Segurança

### O que está protegido:
- ✅ Email do remetente
- ✅ Senha de aplicativo
- ✅ Credenciais SMTP

### O que NÃO é sensível:
- ✅ Servidor SMTP (smtp.gmail.com)
- ✅ Porta (587)
- ✅ Configurações gerais

---

## 🐛 Solução de Problemas

### Erro: "Credenciais SMTP não configuradas"

**Causa:** Arquivo `.env` não existe ou está vazio

**Solução:**
```bash
# Verificar se o arquivo existe
ls -la .env

# Se não existir, criar a partir do exemplo
cp .env.example .env

# Editar e preencher as credenciais
notepad .env
```

### Erro: "Não foi possível carregar .env"

**Causa:** Arquivo mal formatado

**Solução:**
- Verificar que cada linha está no formato `KEY=VALUE`
- Não usar espaços antes/depois do `=`
- Usar aspas apenas se necessário

---

## 📦 Distribuição

### Para Desenvolvimento:
Cada desenvolvedor deve ter seu próprio `.env` com suas credenciais.

### Para Produção (Instalador):
O instalador cria o `config/settings.json` com as credenciais padrão da BEL (configuradas no `setup_script.iss`).

---

## 🔄 Atualizando Credenciais

### Método 1: Editar .env
```bash
notepad .env
```

### Método 2: Usar interface do programa
- Abrir programa
- Menu: Ferramentas → Configurações
- Aba: Email/SMTP
- Atualizar credenciais
- Salvar

**Observação:** Configurações da interface são salvas em `config/settings.json` e têm prioridade sobre `.env`.

---

## 📚 Mais Informações

- **Documentação Completa:** `GUIA_ATUALIZACOES.md`
- **Distribuição:** `GUIA_DISTRIBUICAO.md`
- **Licença:** `license.txt`

