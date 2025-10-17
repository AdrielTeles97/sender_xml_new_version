# 🔐 Como Funcionam as Credenciais no Sistema

## 📖 Visão Geral

O sistema utiliza **dois locais** para armazenar/carregar configurações:

1. **`.env`** - Credenciais sensíveis (email/senha) - **NÃO versionado no Git**
2. **`config/settings.json`** - Outras configurações (caminhos, UI, etc) - Versionado

---

## 🔄 Fluxo de Carregamento

### 1️⃣ Ao Iniciar o Programa (`main.py`)

```python
def _load_default_config(self):
    # 1. Tenta carregar credenciais do .env primeiro
    try:
        from modules.env_config import EnvConfig
        env = EnvConfig()
        smtp_config = env.get_smtp_config()  # ✅ Carrega do .env
    except Exception as e:
        # 2. Se falhar, usa valores vazios
        smtp_config = {
            'server': 'smtp.gmail.com',
            'port': 587,
            'username': '',  # ⚠️ VAZIO
            'password': '',  # ⚠️ VAZIO
            'use_ssl': False
        }

    # 3. Mescla com settings.json (se existir)
    config = self.config_manager.get_config()

    # 4. Se settings.json não tem smtp, usa o do .env
    if 'smtp' not in config or not config['smtp'].get('username'):
        config['smtp'] = smtp_config

    return config
```

**Resultado:**

-   ✅ Credenciais carregadas do `.env`
-   ✅ Outras configurações do `settings.json`
-   ✅ Sistema pronto para enviar emails

---

### 2️⃣ Ao Abrir Configurações (`gui/settings_window.py`)

```python
def _load_settings(self):
    # 1. Carrega do settings.json primeiro
    smtp_config = self.config.get('smtp', {})
    username = smtp_config.get('username', '')  # ⚠️ Pode estar vazio
    password = smtp_config.get('password', '')  # ⚠️ Pode estar vazio

    # 2. Se estiver vazio, busca no .env
    if not username or not password:
        try:
            from modules.env_config import EnvConfig
            env = EnvConfig()
            env_smtp = env.get_smtp_config()
            username = username or env_smtp.get('username', '')  # ✅ Do .env
            password = password or env_smtp.get('password', '')  # ✅ Do .env
        except Exception as e:
            # Mantém vazio se .env não existir
            pass

    # 3. Exibe nos campos
    self.smtp_username_entry.insert(0, username)
    self.smtp_password_entry.insert(0, password)
```

**Resultado:**

-   ✅ Se `settings.json` tem credenciais → usa elas
-   ✅ Se `settings.json` está vazio → busca no `.env`
-   ✅ Usuário vê os valores preenchidos na interface

---

### 3️⃣ Ao Salvar Configurações

Quando o usuário clica em **"Salvar"** nas configurações:

```python
def _save_settings(self):
    self.config['smtp'] = {
        'server': self.smtp_server_entry.get().strip(),
        'port': int(self.smtp_port_entry.get().strip() or 587),
        'username': self.smtp_username_entry.get().strip(),  # 💾 Salva no JSON
        'password': self.smtp_password_entry.get().strip(),  # 💾 Salva no JSON
        'use_ssl': self.smtp_ssl_var.get()
    }

    self.config_manager.save_config(self.config)  # 📝 Grava settings.json
```

**⚠️ ATENÇÃO:**

-   As credenciais são salvas no `settings.json`
-   Isso **sobrescreve** o comportamento do `.env`
-   Na próxima vez, vai carregar do `settings.json`, não do `.env`

---

## 🎯 Prioridade de Carregamento

```
1. settings.json (se tiver username/password preenchidos)
   ↓
2. .env (se settings.json estiver vazio)
   ↓
3. Valores padrão vazios (se nenhum dos anteriores existir)
```

---

## 📁 Estrutura de Arquivos

### `.env` (Credenciais - **NÃO versionado**)

```env
SMTP_USERNAME=belinformatica2019@gmail.com
SMTP_PASSWORD=ztkn jhra empm qbhk
```

### `config/settings.json` (Configurações - Versionado)

```json
{
  "smtp": {
    "server": "smtp.gmail.com",
    "port": 587,
    "username": "",  // ← Vazio para usar .env
    "password": "",  // ← Vazio para usar .env
    "use_ssl": false
  },
  "base_path": "C:\\DigiSat\\SuiteG6\\Servidor\\DFe",
  "ui": { ... }
}
```

---

## 🔒 Segurança

### ✅ O que está PROTEGIDO:

-   `.env` está no `.gitignore` → NÃO vai para GitHub
-   Credenciais do `.env` só existem localmente
-   `.env.example` (sem senhas) é versionado como template

### ⚠️ O que precisa de ATENÇÃO:

-   Se salvar nas configurações, vai para `settings.json`
-   `settings.json` **É versionado** (mas já está com credenciais vazias)
-   Não commite `settings.json` com credenciais preenchidas

---

## 🛠️ Como Usar Corretamente

### Para Desenvolvimento:

1. Copie `.env.example` para `.env`
2. Preencha suas credenciais no `.env`
3. **NUNCA** modifique o `.env.example` com credenciais reais
4. Mantenha `settings.json` com campos `username` e `password` vazios

### Para Produção (Executável):

1. O `.env` é incluído no executável (via PyInstaller)
2. As credenciais vão dentro do `.exe`
3. Usuário final **NÃO vê** o `.env`
4. Mas pode alterar nas configurações (salva no `settings.json` local)

---

## 🐛 Solução de Problemas

### Campos de email/senha aparecem vazios nas configurações:

**Causa:**

-   `settings.json` tem campos vazios
-   `.env` não existe ou está mal configurado

**Solução:**

1. Verifique se `.env` existe na raiz do projeto
2. Confirme que tem:
    ```env
    SMTP_USERNAME=seu_email@gmail.com
    SMTP_PASSWORD=sua_senha_app
    ```
3. Reinicie o programa

### Erro "ModuleNotFoundError: No module named 'dotenv'":

**Causa:**

-   Biblioteca `python-dotenv` não instalada

**Solução:**

```bash
.\venv_sender\Scripts\python.exe -m pip install python-dotenv
```

### Credenciais não funcionam:

**Causa:**

-   Senha de app do Gmail incorreta
-   Conta sem verificação em 2 etapas

**Solução:**

1. Acesse: https://myaccount.google.com/apppasswords
2. Gere nova senha de app
3. Use formato: `xxxx xxxx xxxx xxxx`

---

## 📝 Checklist de Segurança

Antes de fazer commit:

-   [ ] `.env` está no `.gitignore`
-   [ ] `settings.json` tem `username` e `password` vazios
-   [ ] `.env.example` não tem credenciais reais
-   [ ] Não há senhas no código-fonte

Antes de gerar executável:

-   [ ] `.env` existe e está correto
-   [ ] `XMLSender.spec` inclui `.env` nos `datas`
-   [ ] `requirements.txt` tem `python-dotenv>=1.0.0`
-   [ ] Testou o executável gerado

---

## 🔗 Arquivos Relacionados

-   **`modules/env_config.py`** - Carrega variáveis do `.env`
-   **`main.py`** - Inicializa com credenciais do `.env`
-   **`gui/settings_window.py`** - Exibe credenciais na UI
-   **`config/settings.json`** - Armazena configurações gerais
-   **`.env`** - Credenciais locais (não versionado)
-   **`.env.example`** - Template público
-   **`.gitignore`** - Ignora `.env`

---

## 💡 Dica Final

**Recomendação:**

-   Use `.env` para desenvolvimento local
-   Mantenha `settings.json` com campos vazios no Git
-   Usuários finais podem configurar via interface (salva no `settings.json` local deles)

---

Feito com 🔒 por Adriel Teles | BEL Informática
