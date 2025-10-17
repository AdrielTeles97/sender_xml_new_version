# 📋 Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.0.0] - 2025-10-17

### 🎉 Lançamento Inicial

#### ✨ Adicionado
- Sistema completo de envio automático de XMLs do DigiSat Suite G6
- Interface gráfica moderna com CustomTkinter
- Suporte a múltiplos destinatários de email
- Suporte a múltiplos períodos simultâneos
- Organização automática de arquivos (NF-e e NFC-e em pastas separadas)
- Sistema de atualizações automáticas via GitHub Releases
- Histórico completo de envios com banco SQLite
- Agendamento de envios recorrentes
- Máscaras automáticas para CPF (11 dígitos) e CNPJ (14 dígitos)
- Retry automático de emails (até 3 tentativas com backoff exponencial)
- Widget de lista de emails com chips removíveis
- Seletor de múltiplos períodos com interface intuitiva
- Sistema de logs detalhados
- Validação robusta de formulários
- Feedback visual em tempo real
- Dark mode por padrão
- Compactação inteligente com estrutura de pastas

#### 🔒 Segurança
- Sistema de variáveis de ambiente (.env)
- Credenciais protegidas (não versionadas no Git)
- Arquivo .gitignore configurado
- Senha de app do Gmail recomendada
- Validação de formato de email
- Tratamento seguro de exceções

#### 📚 Documentação
- README.md completo e detalhado
- GUIA_ATUALIZACOES.md com passo a passo
- GUIA_DISTRIBUICAO.md para gerar instalador
- README_ENV.md para configuração de credenciais
- CHANGELOG.md (este arquivo)
- Comentários detalhados no código
- Docstrings em todos os métodos

#### 🛠️ Infraestrutura
- Configuração do PyInstaller (XMLSender.spec)
- Script do Inno Setup (setup_script.iss)
- Instalador com desinstalação automática de versão antiga
- Requirements.txt com dependências fixadas
- Estrutura modular e escalável
- Separação de responsabilidades (MVC-like)

#### 🐛 Correções
- Problema de cursor pulando ao digitar CPF/CNPJ
- Erro de encode de emails múltiplos para SMTP
- Detecção de variações de nome de pasta NFe (NF-e, NFe, nfe, etc)
- Layout de emails empilhados verticalmente

#### 🔧 Técnico
- Python 3.14
- CustomTkinter 5.2.0
- Pillow 12.0.0
- Requests 2.32.5
- Packaging 25.0
- SQLite para histórico
- SMTP com TLS
- Arquitetura modular
- Tratamento robusto de erros
- Threading para operações assíncronas

---

## [Unreleased]

### 🔮 Planejado para Próximas Versões

#### v1.1.0 (Planejado)
- [ ] Suporte a exportação de histórico para Excel
- [ ] Filtros avançados no histórico
- [ ] Estatísticas visuais (gráficos)
- [ ] Modo claro (light mode)
- [ ] Suporte a outros provedores de email (Outlook, etc)
- [ ] Configuração de templates de email personalizados
- [ ] Backup automático de configurações

#### v1.2.0 (Planejado)
- [ ] API REST para integração
- [ ] Modo linha de comando (CLI)
- [ ] Notificações desktop
- [ ] Compressão adicional (7z, tar.gz)
- [ ] Suporte a envio via FTP/SFTP
- [ ] Multi-idioma (EN, ES)

#### v2.0.0 (Futuro)
- [ ] Suporte a outros sistemas além do DigiSat
- [ ] Dashboard web
- [ ] App mobile para monitoramento
- [ ] Integração com cloud storage (Google Drive, Dropbox)
- [ ] Sistema de plugins

---

## 📝 Tipos de Mudanças

- **Adicionado** - para novas funcionalidades
- **Modificado** - para mudanças em funcionalidades existentes
- **Descontinuado** - para funcionalidades que serão removidas
- **Removido** - para funcionalidades removidas
- **Corrigido** - para correções de bugs
- **Segurança** - para vulnerabilidades corrigidas

---

## 🔗 Links

- [Repositório](https://github.com/AdrielTeles97/sender_xml_new_version)
- [Releases](https://github.com/AdrielTeles97/sender_xml_new_version/releases)
- [Issues](https://github.com/AdrielTeles97/sender_xml_new_version/issues)
- [Suporte BEL](https://suportebel.com.br)

---

**Nota:** As datas seguem o formato ISO 8601 (AAAA-MM-DD)
