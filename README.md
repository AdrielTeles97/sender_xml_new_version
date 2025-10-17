# 📧 Sistema de Envio Automático de Arquivos XML - DigiSat

<div align="center">

![Version](https://img.shields.io/badge/versão-1.0.0-blue.svg)
![License](https://img.shields.io/badge/licença-Proprietária-red.svg)
![Python](https://img.shields.io/badge/Python-3.14-green.svg)
![Platform](https://img.shields.io/badge/plataforma-Windows-lightgrey.svg)

**Sistema automatizado para envio de arquivos XML (NF-e e NFC-e) do DigiSat Suite G6**

Desenvolvido por Adriel Teles | BEL Informática © 2025

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Configuração](#️-configuração)
- [Estrutura de Diretórios](#-estrutura-de-diretórios)
- [Atualizações](#-atualizações)
- [Solução de Problemas](#-solução-de-problemas)
- [Changelog](#-changelog)
- [Suporte](#-suporte)

---

## 🎯 Sobre o Projeto

Este sistema foi desenvolvido para **facilitar o trabalho de suporte técnico da BEL Informática**, automatizando o processo de envio de arquivos XML de notas fiscais eletrônicas (NF-e e NFC-e) gerados pelo **DigiSat Suite G6**.

### 🔧 Problema Resolvido

Anteriormente, o processo manual de:
1. Navegar pelos diretórios do DigiSat
2. Localizar arquivos XML por período
3. Separar NF-e e NFC-e
4. Compactar arquivos
5. Enviar por email

Era **demorado e propenso a erros**. Este sistema automatiza todo o processo em **poucos cliques**.

### 💡 Solução

Um sistema desktop moderno que:
- ✅ Busca automaticamente os arquivos XML no DigiSat
- ✅ Organiza NF-e e NFC-e em pastas separadas dentro do ZIP
- ✅ Envia por email com formatação profissional
- ✅ Suporta múltiplos períodos e destinatários
- ✅ Mantém histórico de envios
- ✅ Permite agendamento de envios
- ✅ Verifica atualizações automaticamente

---

## ✨ Funcionalidades

### 📁 Busca Inteligente de Arquivos
- Localização automática de XMLs no DigiSat Suite G6
- Suporte a CPF (11 dígitos) e CNPJ (14 dígitos)
- Busca em múltiplos períodos simultaneamente
- Detecção automática de variações de estrutura de diretórios

### 📦 Organização Automática
- **NF-e e NFC-e separados** em pastas dentro do ZIP
- Compactação automática otimizada
- Nomenclatura padronizada: `CNPJ_PERIODO_xmls.zip`

### 📧 Envio Profissional
- Email HTML formatado e responsivo
- **Múltiplos destinatários** suportados
- Anexo automático do ZIP
- Retry automático (até 3 tentativas)
- Suporte a Gmail com senha de app

### 🎨 Interface Moderna
- Design dark/light mode
- Máscaras automáticas para CPF/CNPJ
- Feedback visual em tempo real
- Lista de emails com chips removíveis
- Seletor de múltiplos períodos
- Histórico completo de envios

### 🔄 Sistema de Atualizações
- Verificação automática ao iniciar (após 3s)
- Verificação manual no menu
- Notificação de novas versões
- Download com 1 clique via GitHub Releases

### 📊 Histórico e Agendamento
- Registro de todos os envios (sucesso/erro)
- Filtragem por período, empresa, status
- Estatísticas de envios
- Agendamento de envios recorrentes

---

## 💻 Instalação

### Requisitos
- Windows 10/11 (64-bit)
- 100MB de espaço livre
- Conexão com internet (para envio de emails)

### Passo a Passo

1. **Baixar o Instalador**
   - Acesse: [Releases](https://github.com/AdrielTeles97/sender_xml_new_version/releases)
   - Baixe: `EnvioArquivosXML_Setup_v1.0.0.exe`

2. **Executar o Instalador**
   - Clique duas vezes no arquivo baixado
   - Siga as instruções na tela
   - Se houver versão anterior, será desinstalada automaticamente

3. **Primeiro Acesso**
   - Abra o programa pelo Menu Iniciar ou atalho da área de trabalho
   - Configure o email SMTP (Menu → Ferramentas → Configurações)

---

## 🚀 Como Usar

### 1️⃣ Configuração Inicial

#### Configurar Email de Envio

1. Acesse: **Ferramentas** → **Configurações**
2. Aba: **Email/SMTP**
3. Preencha:
   - Servidor: `smtp.gmail.com`
   - Porta: `587`
   - Email: seu email corporativo
   - Senha: **senha de app** (não a senha normal)
   - SSL: Desativado

#### Como Obter Senha de App do Gmail

1. Acesse: https://myaccount.google.com/security
2. Ative "Verificação em 2 etapas"
3. Acesse: https://myaccount.google.com/apppasswords
4. Crie senha para "Email" no dispositivo "Windows"
5. Copie a senha gerada (formato: `xxxx xxxx xxxx xxxx`)

### 2️⃣ Enviar Arquivos XML

#### Passo a Passo

1. **Selecionar Tipo de Documento**
   - CPF (11 dígitos) ou CNPJ (14 dígitos)

2. **Preencher Dados**
   - **Documento:** Digite CPF ou CNPJ (pode usar máscara)
   - **Nome da Empresa:** Razão social
   - **Email(s):** Digite email e pressione Enter (pode adicionar múltiplos)

3. **Selecionar Período(s)**
   - Escolha ano e mês
   - Clique em **+** para adicionar mais períodos
   - Clique em **🗑️ Remover** para excluir um período

4. **Buscar e Enviar**
   - Clique no botão **"Buscar e Enviar"**
   - Acompanhe o progresso na área de logs
   - Aguarde confirmação de sucesso

### 3️⃣ Verificar Histórico

1. Menu: **Ferramentas** → **Histórico de Envios**
2. Visualize todos os envios realizados
3. Filtre por:
   - Período
   - Empresa
   - Status (Sucesso/Erro)
   - Data

---

## ⚙️ Configuração

### 📂 Caminho Padrão do DigiSat

O sistema busca os XMLs em:
```
C:\DigiSat\SuiteG6\Servidor\DFe\
└── [CNPJ]\
    └── Enviado\
        ├── NFCe\
        │   └── [PERIODO]\
        │       └── Autorizados\
        │           └── *.xml
        └── NFe\  (ou NF-e)
            └── [PERIODO]\
                └── Autorizados\
                    └── *.xml
```

**Exemplo:**
```
C:\DigiSat\SuiteG6\Servidor\DFe\10199836000110\Enviado\NFCe\202510\Autorizados\
```

### 🔧 Alterar Caminho Base

1. Menu: **Ferramentas** → **Configurações**
2. Aba: **Geral**
3. Campo: **Caminho Base dos XMLs**
4. Clique em **Salvar**

---

## 📁 Estrutura de Diretórios

```
sender_xml_new_version/
│
├── 📄 main.py                    # Aplicação principal
├── 📄 requirements.txt           # Dependências Python
├── 📄 .env                       # Credenciais (NÃO versionar)
├── 📄 .env.example              # Template de credenciais
├── 📄 README.md                 # Este arquivo
├── 📄 README_ENV.md             # Documentação de variáveis
├── 📄 GUIA_ATUALIZACOES.md     # Como atualizar o sistema
├── 📄 GUIA_DISTRIBUICAO.md     # Como gerar instalador
│
├── 📁 modules/                   # Módulos do sistema
│   ├── config_manager.py        # Gerenciamento de configurações
│   ├── email_service.py         # Envio de emails
│   ├── xml_finder.py            # Busca de arquivos XML
│   ├── zip_service.py           # Compactação de arquivos
│   ├── history_manager.py       # Histórico de envios
│   ├── env_config.py            # Variáveis de ambiente
│   └── update_checker.py        # Verificação de atualizações
│
├── 📁 gui/                       # Interface gráfica
│   ├── main_window.py           # Janela principal
│   ├── settings_window.py       # Configurações
│   ├── history_window.py        # Histórico
│   ├── schedule_window.py       # Agendamentos
│   ├── period_selector.py       # Seletor de períodos
│   ├── email_list_widget.py     # Lista de emails
│   └── update_window.py         # Janela de atualização
│
├── 📁 config/                    # Configurações
│   └── settings.json            # Configurações do usuário
│
├── 📁 data/                      # Banco de dados
│   └── history.db               # Histórico SQLite
│
├── 📁 logs/                      # Logs da aplicação
│   └── app.log                  # Log principal
│
├── 📁 temp/                      # Arquivos temporários
│   └── *.zip                    # ZIPs gerados (limpos automaticamente)
│
├── 📁 assets/                    # Recursos
│   └── icon.ico                 # Ícone da aplicação
│
├── 📁 dist/                      # Build (PyInstaller)
│   └── XMLSender.exe            # Executável standalone
│
└── 📁 output/                    # Instaladores
    └── EnvioArquivosXML_Setup_v1.0.0.exe
```

---

## 🔄 Atualizações

### Verificação Automática

O sistema verifica automaticamente se há atualizações disponíveis:
- **Quando:** 3 segundos após iniciar o programa
- **Onde:** Busca no GitHub Releases
- **Ação:** Exibe janela se houver nova versão

### Verificação Manual

1. Menu: **Ajuda** → **🔄 Verificar Atualizações**
2. Se houver atualização:
   - Clique em **📥 Baixar Atualização**
   - Feche o programa
   - Execute o novo instalador
   - A versão antiga será desinstalada automaticamente

### Histórico de Versões

Ver arquivo: [CHANGELOG.md](CHANGELOG.md)

---

## 🐛 Solução de Problemas

### Erro: "Credenciais SMTP não configuradas"

**Causa:** Email não configurado

**Solução:**
1. Menu → Ferramentas → Configurações
2. Aba Email/SMTP
3. Preencher todos os campos
4. Salvar

### Erro: "Nenhum arquivo encontrado"

**Causas Possíveis:**
- CNPJ incorreto
- Período sem XMLs
- Caminho do DigiSat incorreto

**Solução:**
1. Verificar CNPJ (11 ou 14 dígitos)
2. Confirmar que o período tem XMLs no DigiSat
3. Menu → Ferramentas → Configurações → Verificar "Caminho Base"

### Erro: "Falha ao enviar email"

**Causas Possíveis:**
- Senha incorreta
- Sem internet
- Limite de envio do Gmail

**Solução:**
1. Verificar senha de app
2. Testar conexão com internet
3. Aguardar alguns minutos (Gmail tem limite de 500 emails/dia)

### Programa não inicia

**Solução:**
1. Reinstalar o programa
2. Verificar antivírus (pode estar bloqueando)
3. Verificar logs em: `%LOCALAPPDATA%\Envio de Arquivos XML\logs\app.log`

---

## 📊 Changelog

### v1.0.0 - Lançamento Inicial (17/10/2024)

#### ✨ Funcionalidades
- Sistema de busca automática de XMLs no DigiSat
- Suporte a CPF e CNPJ com máscaras automáticas
- Múltiplos destinatários de email
- Múltiplos períodos simultâneos
- Organização automática NF-e/NFC-e em pastas
- Sistema de atualizações automáticas via GitHub
- Histórico completo de envios
- Agendamento de envios recorrentes
- Interface moderna com dark mode
- Retry automático de emails (3 tentativas)

#### 🔒 Segurança
- Sistema de variáveis de ambiente (.env)
- Credenciais protegidas (não versionadas)
- Validação de emails
- Logs detalhados

#### 📚 Documentação
- README completo
- Guia de atualizações
- Guia de distribuição
- Documentação de variáveis de ambiente

---

## 💼 Sobre o Desenvolvedor

**Adriel Teles**  
Desenvolvedor | BEL Informática  

📧 Email: adrielt008@gmail.com  
🌐 Website: https://suportebel.com.br  
📱 Suporte: https://suportebel.com.br

---

## 📞 Suporte

### Documentação
- **Guia de Atualizações:** [GUIA_ATUALIZACOES.md](GUIA_ATUALIZACOES.md)
- **Guia de Distribuição:** [GUIA_DISTRIBUICAO.md](GUIA_DISTRIBUICAO.md)
- **Configuração .env:** [README_ENV.md](README_ENV.md)

### Contato
- **Email:** suporte@belinformatica.com.br
- **Website:** https://suportebel.com.br
- **GitHub Issues:** [Reportar Problema](https://github.com/AdrielTeles97/sender_xml_new_version/issues)

### Logs
Logs detalhados estão em:
```
Windows: %LOCALAPPDATA%\Envio de Arquivos XML\logs\app.log
```

---

## 📄 Licença

Copyright © 2025 BEL Informática - Adriel Teles

Todos os direitos reservados. Este software é proprietário e destinado exclusivamente para uso interno da BEL Informática e seus clientes autorizados.

---

## 🙏 Agradecimentos

- **DigiSat** - Sistema de gestão que gera os XMLs
- **BEL Informática** - Equipe de suporte que inspirou este projeto
- **Clientes** - Por utilizarem e confiarem em nossas soluções

---

<div align="center">

**⭐ Se este sistema facilitou seu trabalho, considere deixar uma estrela no repositório!**

Feito com ❤️ por [Adriel Teles](https://github.com/AdrielTeles97)

</div>

