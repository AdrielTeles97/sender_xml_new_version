# 🔄 Sistema de Atualizações Automáticas

## 📋 O que foi implementado

O sistema de atualizações automáticas permite que seus usuários:

-   ✅ Verifiquem manualmente se há atualizações disponíveis
-   ✅ Recebam notificações automáticas ao iniciar o programa
-   ✅ Baixem a nova versão com um clique
-   ✅ Vejam as novidades de cada versão (changelog)

---

## 🛠️ Arquivos Criados/Modificados

### Novos Arquivos:

1. **`modules/update_checker.py`** - Verifica atualizações via GitHub API
2. **`gui/update_window.py`** - Janela de notificação de atualização
3. **`GUIA_ATUALIZACOES.md`** - Este guia

### Arquivos Modificados:

1. **`main.py`** - Verificação automática na inicialização
2. **`gui/main_window.py`** - Menu "Verificar Atualizações"
3. **`requirements.txt`** - Adicionadas dependências `requests` e `packaging`

---

## ⚙️ Configuração Inicial

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install requests>=2.31.0 packaging>=23.0
```

### 2. Configurar Repositório GitHub

**⚠️ IMPORTANTE:** Altere os seguintes locais com suas informações:

#### Em `main.py` (linhas 200-201):

```python
checker = UpdateChecker(
    repo_owner="SEU_USUARIO_GITHUB",  # ← ALTERAR
    repo_name="SEU_REPOSITORIO",       # ← ALTERAR
    current_version=self.app_version
)
```

#### Em `gui/main_window.py` (linhas 878-879):

```python
checker = UpdateChecker(
    repo_owner="SEU_USUARIO_GITHUB",  # ← ALTERAR
    repo_name="SEU_REPOSITORIO",       # ← ALTERAR
    current_version=self.app_version
)
```

---

## 🚀 Como Publicar uma Atualização

### Passo 1: Atualizar a Versão no Código

Em `main.py`, linha 24:

```python
self.app_version = "1.1.0"  # Incrementar versão
```

### Passo 2: Gerar o Executável

```bash
pyinstaller --onefile --windowed --name="XMLSender" --icon=assets/icon.ico main.py
```

### Passo 3: Criar Tag no Git

```bash
git add .
git commit -m "Versão 1.1.0 - Descrição das mudanças"
git tag v1.1.0
git push origin main
git push origin v1.1.0
```

### Passo 4: Criar Release no GitHub

1. Acesse: `https://github.com/SEU_USUARIO/SEU_REPOSITORIO/releases/new`
2. Selecione a tag: `v1.1.0`
3. Título: `Versão 1.1.0 - Título Descritivo`
4. Descrição (Markdown):

    ```markdown
    ## 🎉 Novidades

    -   ✅ Suporte a múltiplos destinatários de email
    -   ✅ Melhorias na interface de períodos
    -   🐛 Correções de bugs

    ## 📦 Como Instalar

    1. Baixe o arquivo `.exe` abaixo
    2. Execute o instalador
    3. Pronto!

    ## 🔧 Melhorias Técnicas

    -   Sistema de atualizações automáticas
    -   Verificação de emails em lista
    -   Organização de arquivos XML por tipo
    ```

5. Anexe o arquivo `.exe` gerado
6. Clique em **"Publish release"**

---

## 🧪 Como Testar

### Teste Manual:

1. Execute o programa
2. Vá em: **Ajuda** → **🔄 Verificar Atualizações**
3. Se houver uma versão mais nova no GitHub, aparecerá uma janela

### Teste Automático:

1. Execute o programa
2. Aguarde 3 segundos
3. Se houver atualização, a janela aparecerá automaticamente

---

## 📊 Versionamento Semântico

Use o formato: `MAJOR.MINOR.PATCH`

-   **MAJOR** (1.x.x): Mudanças incompatíveis com versões anteriores
-   **MINOR** (x.1.x): Novas funcionalidades compatíveis
-   **PATCH** (x.x.1): Correções de bugs

Exemplos:

-   `1.0.0` → Primeira versão
-   `1.1.0` → Adicionar múltiplos emails (nova funcionalidade)
-   `1.1.1` → Corrigir bug de validação (correção)
-   `2.0.0` → Mudança completa na estrutura (breaking change)

---

## 🔒 Segurança

### API do GitHub

-   ✅ A API é pública e segura
-   ✅ Usa HTTPS
-   ✅ Não requer autenticação para leitura
-   ✅ Limite de 60 requisições/hora por IP (suficiente para uso normal)

### Boas Práticas

-   Sempre teste a versão antes de publicar
-   Use releases para versões estáveis
-   Use pre-releases para versões beta
-   Mantenha um changelog atualizado

---

## 🎯 Recursos Disponíveis

### Verificação Manual

-   Menu: **Ajuda** → **🔄 Verificar Atualizações**
-   Verifica instantaneamente
-   Mostra mensagem se já estiver atualizado

### Verificação Automática

-   Ocorre 3 segundos após iniciar o programa
-   Silenciosa (não incomoda se estiver atualizado)
-   Mostra janela apenas se houver atualização

### Janela de Atualização

-   🎉 Visual moderno e atrativo
-   📋 Mostra changelog completo
-   📥 Botão de download direto
-   ⏰ Opção "Mais Tarde"

---

## 🐛 Solução de Problemas

### Erro: "Sem conexão com a internet"

-   Verificar conexão de rede
-   Tentar novamente mais tarde

### Erro: "Nenhum release encontrado"

-   Verificar se criou pelo menos um release no GitHub
-   Verificar se o repositório está público

### Erro: "Tempo esgotado"

-   A API do GitHub pode estar lenta
-   Tentar novamente

### Não aparece atualização mesmo tendo versão nova

-   Verificar se a tag no GitHub tem formato correto: `v1.1.0`
-   Verificar se o `app_version` no código está correto
-   Conferir se `repo_owner` e `repo_name` estão corretos

---

## 📞 Suporte

Em caso de dúvidas ou problemas:

1. Verifique os logs em `logs/app.log`
2. Procure por mensagens do `XMLSender.UpdateChecker`
3. Abra uma issue no GitHub

---

## ✨ Exemplo de Workflow Completo

```bash
# 1. Desenvolver nova funcionalidade
# ... código ...

# 2. Atualizar versão
# Editar main.py: app_version = "1.2.0"

# 3. Testar localmente
python main.py

# 4. Gerar executável
pyinstaller XMLSender.spec

# 5. Commit e tag
git add .
git commit -m "v1.2.0 - Nova funcionalidade X"
git tag v1.2.0
git push origin main --tags

# 6. Criar release no GitHub
# - Acessar GitHub
# - Releases → New Release
# - Anexar .exe
# - Publicar

# 7. Testar atualização
# Executar versão antiga → Deve notificar sobre v1.2.0
```

---

**Pronto! Seu sistema de atualizações está completo e funcional! 🎉**
