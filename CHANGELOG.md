# 📝 Changelog - Sistema de Envio de Arquivos XML

## 🎉 Versão 2.0.0 - Melhorias Significativas (Atual)

### ✨ Novas Funcionalidades

#### 1. 🔄 **Sistema de Retry Automático**

-   **Tentativas automáticas** em caso de falha no envio de email
-   **Backoff exponencial**: Aguarda progressivamente mais tempo entre tentativas
-   **Configurável**: 3 tentativas por padrão, intervalo de 5 segundos
-   **Feedback visual**: Mostra tentativa atual durante o processo
-   **Exemplo**: Se a primeira tentativa falhar, aguarda 5s. Segunda falha? Aguarda 10s.

#### 2. 📊 **Histórico de Envios com SQLite**

-   **Banco de dados local** para registrar todos os envios
-   **Informações armazenadas**:
    -   Data/hora do envio
    -   Documento (CPF/CNPJ)
    -   Empresa
    -   Período
    -   Destinatários
    -   Quantidade de arquivos (NFCe e NFe separados)
    -   Status (sucesso/erro)
    -   Número de tentativas
    -   Mensagem de erro (se houver)
    -   Tempo de processamento
-   **Estatísticas**:
    -   Total de envios
    -   Taxa de sucesso
    -   Total de arquivos enviados
    -   Último envio
-   **Interface gráfica** para visualização e filtros
-   **Limpeza automática** de registros antigos (90 dias)

#### 3. 📧 **Múltiplos Destinatários**

-   **Widget moderno** com tags/chips visuais
-   **Adicione vários emails** pressionando Enter ou clicando no botão +
-   **Validação automática** de formato de email
-   **Remoção fácil**: Clique no X em cada chip
-   **Suporte visual**: Veja todos os destinatários de forma clara

#### 4. 📅 **Sistema de Agendamento**

-   **Agende envios** para datas/horas futuras
-   **Envios recorrentes**:
    -   Diariamente
    -   Semanalmente
    -   Mensalmente
-   **Observações** personalizadas para cada agendamento
-   **Gerenciamento**: Visualize, edite e cancele agendamentos
-   **Execução automática**: Sistema verifica e executa agendamentos pendentes

#### 5. 📈 **Janela de Histórico**

-   **Interface moderna** com tabela organizada
-   **Filtros avançados**:
    -   Por status (sucesso/erro)
    -   Por documento (CPF/CNPJ)
    -   Por período (hoje, últimos 7/30/90 dias)
-   **Estatísticas em tempo real** em cards visuais
-   **Detalhes de erro**: Clique em um registro com erro para ver detalhes
-   **Exportação** (em desenvolvimento)

### 🔧 Melhorias de Correção de Bugs

#### 1. ❌ **Correção do Loop Infinito**

-   **Timeout reduzido** de 30s para 15s nas conexões SMTP
-   **Tratamento robusto** de timeouts e erros de conexão
-   **Mensagens claras** quando há problemas de conectividade

#### 2. 🎨 **Interface Responsiva**

-   **Barra de progresso animada** durante processamento
-   **Botão de enviar desabilitado** enquanto processa
-   **Botão de cancelar** aparece durante processamento
-   **Feedback constante** na área de status

#### 3. 🛡️ **Tratamento de Erros Aprimorado**

-   **Captura global** de exceções não tratadas
-   **Mensagens descritivas** com tipo de erro e solução
-   **Logs detalhados** com stack trace completo
-   **Alertas visuais** para o usuário

#### 4. ⚙️ **Configuração SSL/TLS Corrigida**

-   **Porta 587 agora usa TLS** (corrigido de SSL)
-   **Detecção automática** para Gmail
-   **Mensagens claras** sobre configuração incorreta

### 📁 Novos Arquivos Criados

```
modules/
  └── history_manager.py       # Gerenciamento do banco de dados e histórico

gui/
  ├── email_list_widget.py     # Widget de múltiplos emails com chips
  ├── history_window.py        # Janela de visualização do histórico
  └── schedule_window.py       # Janela de agendamento

data/
  └── history.db               # Banco de dados SQLite (criado automaticamente)
```

### 🗄️ Estrutura do Banco de Dados

#### Tabela: `envios`

-   `id`: ID único
-   `data_envio`: Data/hora do envio
-   `documento`: CPF/CNPJ
-   `empresa`: Nome da empresa
-   `periodo`: Período (YYYY-MM)
-   `destinatarios`: Lista de emails (separados por ;)
-   `total_arquivos`: Total de arquivos
-   `nfce_count`: Quantidade de NFCe
-   `nfe_count`: Quantidade de NFe
-   `status`: Status (sucesso/erro/parcial)
-   `tentativas`: Número de tentativas
-   `erro`: Mensagem de erro (se houver)
-   `arquivo_zip`: Caminho do arquivo ZIP
-   `tempo_processamento`: Tempo em segundos
-   `observacoes`: Observações adicionais

#### Tabela: `agendamentos`

-   `id`: ID único
-   `data_criacao`: Data de criação
-   `data_agendada`: Data/hora agendada
-   `documento`: CPF/CNPJ
-   `empresa`: Nome da empresa
-   `periodos`: Lista de períodos (JSON)
-   `destinatarios`: Lista de emails (JSON)
-   `status`: Status (pendente/executado/cancelado)
-   `executado_em`: Data de execução
-   `recorrente`: Se é recorrente (boolean)
-   `recorrencia_tipo`: Tipo (diaria/semanal/mensal)
-   `ativo`: Se está ativo
-   `observacoes`: Observações

### 🎯 Como Usar as Novas Funcionalidades

#### Múltiplos Destinatários

1. No campo "Email(s)", digite um email
2. Pressione Enter ou clique no botão +
3. O email aparecerá como um chip azul
4. Repita para adicionar mais emails
5. Clique no X para remover

#### Histórico

1. Menu **Ferramentas** → **Histórico de Envios**
2. Use os filtros para encontrar envios específicos
3. Clique em registros com erro para ver detalhes
4. Use **Limpar Antigos** para remover registros de +90 dias

#### Agendamento

1. Menu **Ferramentas** → **Agendar Envio**
2. Configure data e hora futura
3. Marque "Envio recorrente" se necessário
4. Selecione o tipo de recorrência
5. Adicione observações
6. Clique em **Agendar**

### ⚙️ Configurações de Retry

No arquivo `config/settings.json`:

```json
{
    "retry": {
        "max_tentativas": 3, // Número máximo de tentativas
        "intervalo_segundos": 5, // Intervalo base entre tentativas
        "ativo": true // Se o retry está ativo
    }
}
```

### 📊 Estatísticas do Sistema

Ao abrir o Histórico, você verá:

-   🔢 **Total de Envios**: Quantidade total de envios realizados
-   ✅ **Bem-sucedidos**: Envios que foram entregues
-   ❌ **Com Erro**: Envios que falharam
-   📈 **Taxa de Sucesso**: Percentual de sucesso
-   📦 **Arquivos Enviados**: Total de XMLs enviados

### 🚀 Melhorias de Performance

-   **Conexões mais rápidas**: Timeout reduzido para 15s
-   **Retry inteligente**: Backoff exponencial evita sobrecarga
-   **Thread separada**: Interface não trava durante processamento
-   **Banco de dados indexado**: Queries rápidas mesmo com muitos registros

### 🛠️ Próximas Funcionalidades (Roadmap)

-   [ ] Exportação de histórico para CSV/Excel
-   [ ] Dashboard com gráficos de estatísticas
-   [ ] Notificações por email sobre agendamentos
-   [ ] Backup automático do banco de dados
-   [ ] Templates personalizáveis de email
-   [ ] Suporte a anexos adicionais

---

## 📌 Versão 1.0.0 - Versão Inicial

### Funcionalidades Básicas

-   Envio de arquivos XML por email
-   Seleção de múltiplos períodos
-   Compactação automática em ZIP
-   Organização por tipo (NFCe/NFe)
-   Configurações SMTP
-   Interface gráfica moderna com CustomTkinter

---

## 💡 Notas de Atualização

### Migração de 1.0 para 2.0

1. **Banco de dados**: Será criado automaticamente na primeira execução
2. **Configurações**: Novas chaves adicionadas automaticamente
3. **Interface**: Campo de email substituído por widget de múltiplos emails
4. **Compatibilidade**: Mantém retrocompatibilidade com envios de um único email

### Requisitos

-   Python 3.8+
-   customtkinter 5.2.2+
-   Todas as dependências no `requirements.txt`

---

**Desenvolvido por:** Adriel Teles  
**Data:** Outubro 2025  
**Licença:** Proprietária
