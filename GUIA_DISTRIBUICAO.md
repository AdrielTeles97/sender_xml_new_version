# 📦 Guia Completo de Distribuição e Atualização

## 🎯 Estratégia de Distribuição

### **O que colocar no GitHub Release?**

✅ **INSTALADOR (Setup.exe)** - Recomendado!

**Vantagens:**

-   ✅ Desinstala versão antiga automaticamente
-   ✅ Cria atalhos profissionais
-   ✅ Registro em "Adicionar/Remover Programas"
-   ✅ Gerencia arquivos de configuração
-   ✅ Melhor experiência do usuário

---

## 🔄 Como Funciona a Atualização?

### **Do ponto de vista do usuário:**

```
1. Usuário abre o programa
   ↓
2. Sistema verifica atualizações (após 3s)
   ↓
3. 🎉 Aparece: "Nova versão disponível!"
   ↓
4. Usuário clica: "📥 Baixar Atualização"
   ↓
5. Abre navegador → GitHub Release
   ↓
6. Download: EnvioArquivosXML_Setup_v1.1.0.exe
   ↓
7. Usuário executa o instalador
   ↓
8. Instalador detecta versão antiga
   ↓
9. Pergunta: "Desinstalar versão anterior?"
   ↓
10. Desinstala automaticamente
    ↓
11. Instala nova versão
    ↓
12. ✅ Pronto! Atualizado!
```

### **Isto é normal?**

**SIM!** É assim que funciona em softwares profissionais:

-   Google Chrome
-   Discord
-   Visual Studio Code
-   Spotify
-   Todos fazem assim!

---

## 🚀 Processo Completo de Compilação

### **1. Gerar Executável (PyInstaller)**

```bash
# No ambiente virtual
.\venv_sender\Scripts\python.exe -m PyInstaller XMLSender.spec --clean --noconfirm
```

**Resultado:** `dist\XMLSender.exe` (executável standalone ~50MB)

### **2. Gerar Instalador (Inno Setup)**

```bash
# Se tiver Inno Setup instalado e no PATH:
iscc setup_script.iss

# OU abrir manualmente:
# 1. Abrir Inno Setup Compiler
# 2. Abrir setup_script.iss
# 3. Build → Compile
```

**Resultado:** `output\EnvioArquivosXML_Setup_v1.0.0.exe` (instalador ~25MB)

---

## 📝 Workflow Completo - Passo a Passo

### **Publicar Nova Versão (Ex: v1.1.0)**

#### **Passo 1: Atualizar Código**

1. **Desenvolver nova funcionalidade**
2. **Atualizar versão** em `main.py`:
    ```python
    self.app_version = "1.1.0"  # ← Incrementar
    ```
3. **Testar localmente**

#### **Passo 2: Gerar Executável**

```bash
.\venv_sender\Scripts\python.exe -m PyInstaller XMLSender.spec --clean --noconfirm
```

Verificar: `dist\XMLSender.exe`

#### **Passo 3: Atualizar Script Inno Setup**

Editar `setup_script.iss` linha 4:

```inno
#define MyAppVersion "1.1.0"  ← Atualizar aqui
```

#### **Passo 4: Gerar Instalador**

```bash
iscc setup_script.iss
```

Verificar: `output\EnvioArquivosXML_Setup_v1.1.0.exe`

#### **Passo 5: Commit e Tag**

```bash
git add .
git commit -m "v1.1.0 - Descrição das mudanças"
git tag v1.1.0
git push origin main
git push origin v1.1.0
```

#### **Passo 6: Criar Release no GitHub**

1. **Acessar:** `https://github.com/SEU_USUARIO/SEU_REPO/releases/new`

2. **Configurar:**

    - **Tag:** `v1.1.0`
    - **Título:** `Versão 1.1.0 - Melhorias e Correções`
    - **Descrição:**

        ```markdown
        ## 🎉 Novidades

        -   ✅ Sistema de atualizações automáticas
        -   ✅ Suporte a múltiplos destinatários de email
        -   ✅ Interface melhorada para emails
        -   🐛 Correções de bugs

        ## 📥 Como Instalar

        1. Baixe o arquivo `EnvioArquivosXML_Setup_v1.1.0.exe` abaixo
        2. Execute o instalador
        3. Se houver versão anterior, será desinstalada automaticamente
        4. Pronto!

        ## 📋 Requisitos

        -   Windows 10/11
        -   100MB de espaço livre
        ```

3. **Anexar arquivo:**

    - `output\EnvioArquivosXML_Setup_v1.1.0.exe`

4. **Publicar:** Clicar em "Publish release"

---

## 🧪 Testar Sistema de Atualizações

### **Teste 1: Simular Nova Versão**

1. Criar release de teste com versão `v999.0.0`
2. Executar seu programa (versão 1.0.0)
3. Ir em: **Ajuda** → **🔄 Verificar Atualizações**
4. Deve aparecer: "Versão 999.0.0 está disponível!"

### **Teste 2: Processo Completo**

1. Instalar versão 1.0.0
2. Publicar versão 1.1.0 no GitHub
3. Abrir programa versão 1.0.0
4. Aguardar notificação automática
5. Clicar "Baixar Atualização"
6. Instalar nova versão
7. Verificar que está na versão 1.1.0

---

## 📊 Comparação: Executável vs Instalador

| Característica         | Executável (.exe) | Instalador (Setup.exe) |
| ---------------------- | ----------------- | ---------------------- |
| Tamanho                | ~50MB             | ~25MB                  |
| Atalhos                | ❌ Manual         | ✅ Automático          |
| Desinstalador          | ❌ Não            | ✅ Sim                 |
| Registro Windows       | ❌ Não            | ✅ Sim                 |
| Atualização            | ⚠️ Manual         | ✅ Automatizada        |
| Profissional           | ⚠️ Médio          | ✅ Alto                |
| **Recomendado GitHub** | ❌ Não            | ✅ **SIM**             |

---

## 🔧 Arquivos Importantes

### **Geração:**

-   `XMLSender.spec` - Configuração do PyInstaller
-   `setup_script.iss` - Configuração do Inno Setup

### **Saída:**

-   `dist\XMLSender.exe` - Executável standalone
-   `output\EnvioArquivosXML_Setup_v1.0.0.exe` - Instalador final

### **Controle de Versão:**

-   `main.py` (linha 24) - Versão no código Python
-   `setup_script.iss` (linha 4) - Versão no instalador

**⚠️ IMPORTANTE:** Manter ambas sincronizadas!

---

## 💡 Dicas Profissionais

### **Versionamento:**

Use **Semantic Versioning**: `MAJOR.MINOR.PATCH`

-   `1.0.0` → `1.1.0` - Nova funcionalidade
-   `1.1.0` → `1.1.1` - Correção de bug
-   `1.1.1` → `2.0.0` - Mudança incompatível

### **Changelog:**

Sempre documente mudanças na descrição do release:

```markdown
## 🎉 Novidades

-   Nova funcionalidade X
-   Melhoria em Y

## 🐛 Correções

-   Corrigido bug Z
-   Resolvido problema W

## ⚠️ Mudanças Importantes

-   Descontinuado recurso antigo
```

### **Testes Antes de Publicar:**

1. ✅ Testar instalador em máquina limpa
2. ✅ Verificar se todos os recursos funcionam
3. ✅ Testar desinstalação
4. ✅ Testar atualização de versão anterior

---

## 🚨 Solução de Problemas

### **Erro: "Arquivo executável não encontrado"**

-   Verificar se rodou PyInstaller com sucesso
-   Checar se `dist\XMLSender.exe` existe
-   Verificar caminhos no `setup_script.iss`

### **Instalador não detecta versão antiga**

-   Verificar se `AppId` está igual nas duas versões
-   Checar registro do Windows

### **Programa não inicia após instalação**

-   Verificar se todas as dependências foram incluídas
-   Testar executável `dist\XMLSender.exe` diretamente
-   Verificar logs em `%LOCALAPPDATA%\Envio de Arquivos XML\logs\`

---

## 📦 Checklist de Distribuição

Antes de publicar uma release:

-   [ ] Código testado e funcionando
-   [ ] Versão atualizada em `main.py`
-   [ ] Versão atualizada em `setup_script.iss`
-   [ ] Executável gerado com PyInstaller
-   [ ] Instalador gerado com Inno Setup
-   [ ] Instalador testado em máquina limpa
-   [ ] Changelog preparado
-   [ ] Tag criada no Git
-   [ ] Release criada no GitHub
-   [ ] Instalador anexado ao release
-   [ ] Testado processo de atualização

---

## 🎯 Resumo

**Para distribuir nova versão:**

1. Incrementar versão no código
2. Gerar executável (PyInstaller)
3. Gerar instalador (Inno Setup)
4. Criar tag e release no GitHub
5. Anexar **INSTALADOR** (não o .exe)
6. Usuários recebem notificação automática
7. Download e instalação com 1 clique

**Simples e Profissional! 🚀**
