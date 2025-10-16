# 📘 Manual de Uso - Sistema de Envio de Arquivos XML v2.0

## 🚀 Início Rápido

### 1. Configuração Inicial

#### Passo 1: Configurar SMTP

1. Abra o menu **Ferramentas** → **Configurações**
2. Preencha os dados do servidor SMTP:
    - **Servidor**: `smtp.gmail.com` (para Gmail)
    - **Porta**: `587` (para TLS) ou `465` (para SSL)
    - **Usuário**: Seu email completo
    - **Senha**: Senha de aplicativo (veja abaixo)
    - **Usar SSL**: Desmarque para porta 587, marque para 465

**⚠️ Para Gmail:**

-   Use uma **Senha de Aplicativo**, não sua senha normal
-   Acesse: https://myaccount.google.com/security
-   Vá em: Verificação em duas etapas → Senhas de app
-   Gere uma senha para "Aplicativo de desktop"

3. Clique em **Testar SMTP** para verificar
4. Clique em **Salvar**

#### Passo 2: Configurar Diretório Base

1. Na mesma janela de Configurações
2. Aba **Diretórios**
3. Defina o caminho base dos XMLs
    - Padrão: `C:\DigiSat\SuiteG6\Servidor\DFe`
4. Clique em **Salvar**

---

## 📧 Envio Básico de XMLs

### Passo a Passo

1. **Preencha os Dados**

    - **CPF/CNPJ**: Digite o documento (formatação automática)
    - **Nome da Empresa**: Nome completo
    - **Email(s)**: Adicione um ou mais destinatários

2. **Adicionar Emails**

    - Digite o email no campo
    - Pressione **Enter** ou clique em **+**
    - Repita para adicionar mais emails
    - Clique no **X** em cada chip para remover

3. **Selecionar Períodos**

    - Use os dropdowns de Ano e Mês
    - Clique em **+** para adicionar mais períodos
    - Clique no **X** para remover períodos

4. **Enviar**
    - Clique em **Buscar e Enviar**
    - Acompanhe o progresso na área de Status
    - A barra de progresso mostra que está processando
    - Use **Cancelar** se precisar interromper

### Exemplo de Feedback

```
[10:30:45] Iniciando busca para CPF/CNPJ: 19.359.762.0001/07
[10:30:45] Períodos selecionados: 2025-01
[10:30:45] Destinatários: email1@example.com, email2@example.com
[10:30:46] Buscando arquivos para o período: 202501
[10:30:46] Encontrados 5 arquivos NFC-e e 3 arquivos NF-e
[10:30:47] Compactando 8 arquivos organizados por tipo...
[10:30:48] 📧 Enviando para 2 destinatário(s): email1@example.com, email2@example.com
[10:30:53] ✅ Envio concluído com sucesso! (1/1)
[10:30:53] 📦 Arquivo enviado com estrutura organizada:
[10:30:53]    📁 NFCe/ (5 arquivos)
[10:30:53]    📁 NFe/ (3 arquivos)
[10:30:53] 🎉 Processamento concluído com sucesso! 1/1 períodos enviados.
```

---

## 🔄 Sistema de Retry Automático

### Como Funciona

Quando um envio falha, o sistema automaticamente:

1. **Aguarda** um intervalo antes de tentar novamente
2. **Tenta novamente** até 3 vezes (configurável)
3. **Aumenta o intervalo** entre tentativas (backoff exponencial)
4. **Informa** o usuário sobre cada tentativa

### Exemplo com Retry

```
[10:30:48] 📧 Enviando para 1 destinatário(s): email@example.com
[10:30:53] 🔄 Tentativa 2/3...
[10:31:03] 🔄 Tentativa 3/3...
[10:31:18] ✅ Envio concluído com sucesso!
[10:31:18]    ℹ️ Sucesso após 3 tentativa(s)
```

### Configurar Retry

Edite `config/settings.json`:

```json
{
    "retry": {
        "max_tentativas": 3, // Tente até 3 vezes
        "intervalo_segundos": 5, // Aguarde 5s, depois 10s, depois 15s...
        "ativo": true // true = ativo, false = desativado
    }
}
```

---

## 📊 Visualizar Histórico

### Acessar Histórico

1. Menu **Ferramentas** → **Histórico de Envios**
2. Veja todos os envios já realizados

### Usar Filtros

-   **Status**: Filtre por Sucesso, Erro ou Parcial
-   **Documento**: Digite CPF/CNPJ para filtrar
-   **Período**: Hoje, Últimos 7/30/90 dias

### Estatísticas

No topo da janela, veja:

-   🔢 Total de envios realizados
-   ✅ Envios bem-sucedidos
-   ❌ Envios com erro
-   📈 Taxa de sucesso (%)
-   📦 Total de arquivos enviados

### Ver Detalhes de Erro

-   Clique em qualquer linha com erro (texto vermelho)
-   Uma janela mostrará os detalhes completos do erro

### Limpeza

-   **Limpar Antigos**: Remove registros com mais de 90 dias
-   **Confirmação**: Sistema pede confirmação antes de remover

---

## 📅 Agendar Envios Automáticos

### Criar Agendamento

1. Menu **Ferramentas** → **Agendar Envio**
2. **Configure a Data e Hora**:
    - Dia/Mês/Ano
    - Hora:Minuto (formato 24h)
3. **Recorrência** (opcional):
    - Marque "Envio recorrente"
    - Selecione: Diariamente, Semanalmente ou Mensalmente
4. **Observações**: Adicione notas sobre o agendamento
5. Clique em **Agendar**

### Exemplo de Agendamento

**Cenário**: Enviar XMLs todo dia 1º às 08:00

1. Data: `01/01/2026` (próximo mês)
2. Hora: `08:00`
3. Marcar "Envio recorrente"
4. Tipo: "Mensalmente"
5. Observação: "Envio mensal automático"

### Notas Importantes

⚠️ **O agendamento usa os dados do formulário principal:**

-   Documento, Empresa e Emails configurados no momento
-   Períodos serão determinados automaticamente no momento do envio
-   Certifique-se de que os dados estão corretos antes de agendar

### Gerenciar Agendamentos

-   **Ver Agendamentos**: Clique no botão "📋 Ver Agendamentos"
-   **Cancelar**: Cancele agendamentos que não são mais necessários
-   **Status**: Veja quais foram executados e quais estão pendentes

---

## 💡 Dicas e Melhores Práticas

### 📧 Emails

✅ **Boas Práticas:**

-   Adicione apenas emails válidos
-   Verifique a caixa de spam dos destinatários na primeira vez
-   Use múltiplos destinatários para backup

❌ **Evite:**

-   Emails com formato inválido
-   Muitos destinatários de uma vez (máx. 10 recomendado)

### 📁 Arquivos

✅ **Organize Bem:**

-   Mantenha a estrutura de pastas correta
-   Verifique se os XMLs estão nos diretórios corretos
-   Use o debug do sistema para verificar caminhos

### 🔄 Retry

✅ **Quando Usar:**

-   Conexões instáveis
-   Servidores SMTP temporariamente indisponíveis
-   Problemas intermitentes de rede

❌ **Quando Desativar:**

-   Emails de teste frequentes
-   Debugging do sistema
-   Economizar tempo em desenvolvimento

### 📊 Histórico

✅ **Manutenção:**

-   Limpe registros antigos periodicamente
-   Exporte dados importantes antes de limpar
-   Use filtros para encontrar problemas recorrentes

### 📅 Agendamentos

✅ **Planejamento:**

-   Agende com antecedência
-   Use recorrência para tarefas repetitivas
-   Adicione observações claras
-   Teste manualmente antes de agendar

---

## 🆘 Solução de Problemas

### ❌ "Erro de autenticação SMTP"

**Problema**: Senha ou usuário incorretos

**Solução:**

1. Verifique se está usando **Senha de Aplicativo** (Gmail)
2. Verifique se o email está correto
3. Tente o botão "Testar SMTP" nas configurações
4. Para Gmail, ative a verificação em 2 etapas primeiro

---

### ❌ "Tempo de conexão esgotado"

**Problema**: Servidor SMTP não responde em 15 segundos

**Solução:**

1. Verifique sua conexão com a internet
2. Confirme servidor e porta corretos
3. Firewall pode estar bloqueando
4. Tente trocar porta 587 ↔ 465

---

### ❌ "Nenhum arquivo encontrado"

**Problema**: Sistema não encontra XMLs

**Solução:**

1. Verifique o "Diretório Base" nas configurações
2. Confirme que os XMLs estão em:
    ```
    {Base}\{CPF_CNPJ}\Enviado\NFCe\{AAAAMM}\Autorizados\
    {Base}\{CPF_CNPJ}\Enviado\NFe\{AAAAMM}\Autorizados\
    ```
3. Verifique se o período está correto
4. Confira os logs em `logs/app.log`

---

### ❌ "Erro SSL/TLS"

**Problema**: Configuração SSL incorreta

**Solução:**

-   **Porta 587**: Use **TLS** (desmarque "Usar SSL")
-   **Porta 465**: Use **SSL** (marque "Usar SSL")
-   Gmail: Prefira 587 com TLS desativado

---

### 📋 Logs

Todos os erros são registrados em:

```
logs/app.log
```

Abra este arquivo para ver detalhes completos de erros.

---

## 🎯 Atalhos e Produtividade

### Teclado

-   **Enter** no campo de email: Adiciona email
-   **Esc** em janelas secundárias: Fecha a janela

### Fluxo Rápido

1. `CPF/CNPJ` + `Tab` → `Empresa` + `Tab` → `Email` + `Enter`
2. Selecionar período
3. `Buscar e Enviar`

---

## 📞 Suporte

Para problemas ou dúvidas:

-   **Logs**: Verifique `logs/app.log`
-   **Desenvolvedor**: Adriel Teles
-   **Documentação**: Este manual + `CHANGELOG.md`

---

**Última atualização:** Outubro 2025  
**Versão do Manual:** 2.0.0
