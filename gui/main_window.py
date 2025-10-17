#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import threading
import logging
from datetime import datetime, timedelta
from tkinter import messagebox, Menu

import customtkinter as ctk
from PIL import Image, ImageTk

from modules.xml_finder import XMLFinder
from modules.zip_service import ZipService
from modules.email_service import EmailService
from modules.history_manager import HistoryManager
from gui.settings_window import SettingsWindow
from gui.period_selector import PeriodSelector
from gui.email_list_widget import EmailListWidget
from gui.history_window import HistoryWindow
from gui.schedule_window import ScheduleWindow

class MainWindow:
    """Janela principal da aplicação"""
    
    def __init__(self, root, config, config_manager, app_version, developer, on_exit_callback):
        """
        Inicializa a janela principal.
        
        Args:
            root (CTk): Janela raiz da aplicação
            config (dict): Configurações da aplicação
            config_manager (ConfigManager): Gerenciador de configurações
            app_version (str): Versão da aplicação
            developer (str): Nome do desenvolvedor
            on_exit_callback (function): Função a ser chamada ao fechar a aplicação
        """
        self.root = root
        self.config = config
        self.config_manager = config_manager
        self.app_version = app_version
        self.developer = developer
        self.on_exit_callback = on_exit_callback
        
        self.logger = logging.getLogger("XMLSender.MainWindow")
        
        # Variáveis para os campos do formulário
        self.document_id_var = ctk.StringVar(value=config.get('document_id', ''))
        self.company_var = ctk.StringVar(value=config.get('company_name', ''))
        self.email_var = ctk.StringVar(value=config.get('email', ''))
        
        # Tipo de documento (CPF ou CNPJ)
        self.doc_type_var = ctk.StringVar(value=config.get('doc_type', 'CNPJ'))
        
        # Controle de estado de processamento
        self.is_processing = False
        self.processing_cancelled = False
        self.current_thread = None
        
        # Flag para evitar recursão na formatação de CPF/CNPJ
        self._formatting = False
        
        # Inicializar gerenciador de histórico
        try:
            self.history_manager = HistoryManager()
        except Exception as e:
            self.logger.error(f"Erro ao inicializar histórico: {e}")
            self.history_manager = None
        
        # Definir tamanho da janela para melhor visualização
        self.root.geometry("1100x800")
        self.root.minsize(1000, 700)
        
        # Desabilitar redimensionamento para manter layout fixo
        self.root.resizable(False, False)
        
        # Construir interface
        self._build_interface()
    
    def _build_interface(self):
        """Constrói a interface da janela principal"""
        # Criar menu estilo Windows
        self._create_menu()
        
        # Frame principal com scrollbar para telas pequenas
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True)
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(main_container, height=70, fg_color=("gray85", "gray20"))
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_title = ctk.CTkLabel(
            header_frame,
            text="📧 Envio de Arquivos XML",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header_title.pack(pady=20)
        
        # Container principal dividido em 2 colunas
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configurar grid de 2 colunas: Formulário (esquerda) e Logs (direita)
        content_container.grid_columnconfigure(0, weight=2, minsize=450)  # Formulário
        content_container.grid_columnconfigure(1, weight=3, minsize=550)  # Logs
        content_container.grid_rowconfigure(0, weight=1)
        
        # === COLUNA ESQUERDA: FORMULÁRIO ===
        left_panel = ctk.CTkFrame(content_container)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        form_header = ctk.CTkLabel(
            left_panel,
            text="📋 Dados do Envio",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        form_header.pack(fill="x", padx=15, pady=(15, 10))
        
        # Frame do formulário com scroll
        form_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="transparent", height=400)
        form_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Frame interno para organizar melhor os campos
        form_inner = ctk.CTkFrame(form_scroll, fg_color="transparent")
        form_inner.pack(fill="x", padx=5, pady=5)
        
        # Tipo de Documento (Radio buttons)
        doc_type_label = ctk.CTkLabel(form_inner, text="Tipo:", anchor="e", width=120)
        doc_type_label.grid(row=0, column=0, sticky="e", padx=(10, 5), pady=5)
        
        doc_type_frame = ctk.CTkFrame(form_inner, fg_color="transparent")
        doc_type_frame.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        cpf_radio = ctk.CTkRadioButton(
            doc_type_frame,
            text="CPF (11 dígitos)",
            variable=self.doc_type_var,
            value="CPF",
            command=self._on_doc_type_change
        )
        cpf_radio.pack(side="left", padx=(0, 20))
        
        cnpj_radio = ctk.CTkRadioButton(
            doc_type_frame,
            text="CNPJ (14 dígitos)",
            variable=self.doc_type_var,
            value="CNPJ",
            command=self._on_doc_type_change
        )
        cnpj_radio.pack(side="left")
        
        # CPF/CNPJ
        doc_id_label = ctk.CTkLabel(form_inner, text="Documento:", anchor="e", width=120)
        doc_id_label.grid(row=1, column=0, sticky="e", padx=(10, 5), pady=10)
        self.doc_id_entry = ctk.CTkEntry(form_inner, textvariable=self.document_id_var, width=300, placeholder_text="Digite apenas os números")
        self.doc_id_entry.grid(row=1, column=1, sticky="w", padx=5, pady=10)
        
        # Formatar apenas quando sair do campo (FocusOut) - evita problema de cursor
        self.doc_id_entry.bind("<FocusOut>", self._format_document_id)
        self.doc_id_entry.bind("<Return>", self._format_document_id)
        
        # Nome da Empresa
        company_label = ctk.CTkLabel(form_inner, text="Nome da Empresa:", anchor="e", width=120)
        company_label.grid(row=2, column=0, sticky="e", padx=(10, 5), pady=10)
        company_entry = ctk.CTkEntry(form_inner, textvariable=self.company_var, width=300)
        company_entry.grid(row=2, column=1, sticky="w", padx=5, pady=10)
        
        # Email (Múltiplos Destinatários)
        email_label = ctk.CTkLabel(form_inner, text="Email(s):", anchor="e", width=120)
        email_label.grid(row=3, column=0, sticky="ne", padx=(10, 5), pady=10)
        
        # Widget de múltiplos emails
        self.email_widget = EmailListWidget(form_inner)
        self.email_widget.grid(row=3, column=1, sticky="ew", padx=5, pady=10)
        
        # Adicionar email inicial se houver
        if self.email_var.get():
            self.email_widget.add_email(self.email_var.get())
        
        # Período (usando o componente PeriodSelector)
        period_label = ctk.CTkLabel(form_inner, text="Período(s):", anchor="e", width=120)
        period_label.grid(row=4, column=0, sticky="ne", padx=(10, 5), pady=10)
        
        # Frame para o componente do seletor de período para controlar o tamanho
        period_container = ctk.CTkFrame(form_inner, fg_color="transparent")
        period_container.grid(row=4, column=1, sticky="ew", padx=5, pady=10)
        
        self.period_selector = PeriodSelector(period_container)
        self.period_selector.pack(fill="x", expand=True)
        
        # Auto-salvar configurações ao preencher campos
        self.doc_id_entry.bind("<KeyRelease>", lambda e: self._save_settings(False))
        company_entry.bind("<FocusOut>", lambda e: self._save_settings(False))
        # email_widget não precisa de auto-save (gerencia internamente)
        
        # Ajustar o grid
        form_inner.grid_columnconfigure(0, weight=0)
        form_inner.grid_columnconfigure(1, weight=1)
        
        # Botão de busca e envio
        button_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(5, 15))
        
        # Criar frame para os botões (enviar e cancelar)
        buttons_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        buttons_container.pack()
        
        self.send_button = ctk.CTkButton(
            buttons_container,
            text="Buscar e Enviar",
            command=self._search_and_send,
            width=200,
            height=40
        )
        self.send_button.pack(side="left", padx=5)
        
        # Botão de cancelar (inicialmente oculto)
        self.cancel_button = ctk.CTkButton(
            buttons_container,
            text="Cancelar",
            command=self._cancel_processing,
            width=100,
            height=40,
            fg_color="#D32F2F",
            hover_color="#B71C1C"
        )
        # Não exibir o botão de cancelar inicialmente
        
        # Barra de progresso (inicialmente oculta)
        self.progress_bar = ctk.CTkProgressBar(button_frame, mode="indeterminate")
        # Não exibir inicialmente
        
        # === COLUNA DIREITA: STATUS E LOGS ===
        right_panel = ctk.CTkFrame(content_container)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Header do painel de status
        status_header_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        status_header_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        status_header = ctk.CTkLabel(
            status_header_frame,
            text="📊 Status e Logs",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        status_header.pack(side="left")
        
        # Botão para limpar logs
        clear_logs_btn = ctk.CTkButton(
            status_header_frame,
            text="🗑️ Limpar",
            width=80,
            height=28,
            command=self._clear_status,
            fg_color="gray40",
            hover_color="gray50"
        )
        clear_logs_btn.pack(side="right")
        
        # Frame do status com scroll
        status_frame = ctk.CTkFrame(right_panel)
        status_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        self.status_text = ctk.CTkTextbox(
            status_frame,
            wrap="word",
            font=ctk.CTkFont(size=12, family="Consolas")
        )
        self.status_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # === RODAPÉ ===
        footer_frame = ctk.CTkFrame(main_container, height=35, fg_color=("gray90", "gray15"))
        footer_frame.pack(fill="x", side="bottom", padx=0, pady=0)
        footer_frame.pack_propagate(False)
        
        version_label = ctk.CTkLabel(
            footer_frame,
            text=f"📦 Versão {self.app_version}",
            font=ctk.CTkFont(size=10)
        )
        version_label.pack(side="left", padx=15)
        
        developer_label = ctk.CTkLabel(
            footer_frame,
            text=f"Desenvolvido por: {self.developer} © {datetime.now().year}",
            font=ctk.CTkFont(size=10)
        )
        developer_label.pack(side="right", padx=15)

    def _create_menu(self):
        """Cria o menu estilo Windows padrão"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Salvar Configurações", command=lambda: self._save_settings(True))
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.on_exit_callback)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Ferramentas
        tools_menu = Menu(menubar, tearoff=0)
        tools_menu.add_command(label="📊 Histórico de Envios", command=self._show_history)
        tools_menu.add_command(label="📅 Agendar Envio", command=self._show_schedule)
        tools_menu.add_separator()
        tools_menu.add_command(label="⚙️ Configurações", command=self._show_settings)
        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
        
        # Menu Ajuda
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Ajuda", command=self._show_help)
        help_menu.add_separator()
        help_menu.add_command(label="🔄 Verificar Atualizações", command=self._check_for_updates)
        help_menu.add_separator()
        help_menu.add_command(label="Sobre", command=self._show_about)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
    
    def _show_about(self):
        """Exibe informações sobre o sistema"""
        about_text = (
            f"{self.root.title()}\n\n"
            f"Versão: {self.app_version}\n"
            f"Desenvolvido por: {self.developer}\n"
            f"© {datetime.now().year} Todos os direitos reservados.\n\n"
        )
        
        messagebox.showinfo("Sobre", about_text)
    
    def _on_doc_type_change(self):
        """Callback quando o tipo de documento muda"""
        # Reformatar o documento atual com a nova máscara
        self._format_document_id()
        # Salvar a preferência
        self.config['doc_type'] = self.doc_type_var.get()
    
    def _format_document_id(self, event=None):
        """
        Formata o CPF/CNPJ com máscara baseado no tipo selecionado.
        Executa apenas quando o usuário sai do campo (FocusOut) ou pressiona Enter.
        Isso evita o problema do cursor pular durante a digitação.
        """
        # Pegar valor atual
        current = self.document_id_var.get()
        
        # Extrair apenas dígitos
        digits_only = ''.join(filter(str.isdigit, current))
        
        # Se não tem nada, não fazer nada
        if len(digits_only) == 0:
            return
        
        # Obter tipo selecionado
        doc_type = self.doc_type_var.get()
        
        # Aplicar formatação baseada no tipo
        if doc_type == "CPF":
            # Limitar a 11 dígitos para CPF
            digits_only = digits_only[:11]
            
            # CPF: 000.000.000-00
            if len(digits_only) <= 3:
                formatted = digits_only
            elif len(digits_only) <= 6:
                formatted = f"{digits_only[:3]}.{digits_only[3:]}"
            elif len(digits_only) <= 9:
                formatted = f"{digits_only[:3]}.{digits_only[3:6]}.{digits_only[6:]}"
            else:
                formatted = f"{digits_only[:3]}.{digits_only[3:6]}.{digits_only[6:9]}-{digits_only[9:]}"
        else:  # CNPJ
            # Limitar a 14 dígitos para CNPJ
            digits_only = digits_only[:14]
            
            # CNPJ: 00.000.000/0000-00
            if len(digits_only) <= 2:
                formatted = digits_only
            elif len(digits_only) <= 5:
                formatted = f"{digits_only[:2]}.{digits_only[2:]}"
            elif len(digits_only) <= 8:
                formatted = f"{digits_only[:2]}.{digits_only[2:5]}.{digits_only[5:]}"
            elif len(digits_only) <= 12:
                formatted = f"{digits_only[:2]}.{digits_only[2:5]}.{digits_only[5:8]}/{digits_only[8:]}"
            else:
                formatted = f"{digits_only[:2]}.{digits_only[2:5]}.{digits_only[5:8]}/{digits_only[8:12]}-{digits_only[12:]}"
        
        # Atualizar o valor
        if formatted != current:
            self.document_id_var.set(formatted)
    
    def _show_settings(self):
        """Exibe a janela de configurações"""
        settings_window = SettingsWindow(self.root, self.config, self.config_manager)
    
    def _show_history(self):
        """Exibe a janela de histórico"""
        if self.history_manager:
            history_window = HistoryWindow(self.root, self.history_manager)
        else:
            messagebox.showerror("Erro", "Sistema de histórico não está disponível.")
    
    def _show_schedule(self):
        """Exibe a janela de agendamento"""
        if self.history_manager:
            schedule_window = ScheduleWindow(self.root, self.history_manager, self.config)
        else:
            messagebox.showerror("Erro", "Sistema de agendamento não está disponível.")
    
    def _show_help(self):
        """Exibe a ajuda da aplicação"""
        help_text = (
            "Sistema de Envio de Arquivos XML\n\n"
            "Este sistema permite buscar e enviar arquivos XML de NF-e e NFC-e por email.\n\n"
            "Para utilizar:\n"
            "1. Preencha os dados da empresa e o email de destino\n"
            "2. Selecione um ou mais períodos usando o seletor de datas\n"
            "3. Clique em 'Buscar e Enviar'\n\n"
            "Você pode adicionar múltiplos períodos clicando no botão '+'\n\n"
            "Desenvolvido por: Adriel Teles \n"
        )
        
        messagebox.showinfo("Ajuda", help_text)
    
    def _save_settings(self, show_message=True):
        """
        Salva as configurações atuais.
        
        Args:
            show_message (bool): Se deve mostrar mensagem de sucesso
        """
        # Obter valores sem máscaras para o documento
        doc_id = self.document_id_var.get().strip()
        doc_id_clean = ''.join(filter(str.isdigit, doc_id))
        
        self.config['document_id'] = doc_id
        self.config['document_id_clean'] = doc_id_clean
        self.config['company_name'] = self.company_var.get().strip()
        self.config['email'] = self.email_var.get().strip()
        
        try:
            self.config_manager.save_config(self.config)
            if show_message:
                messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        except Exception as e:
            self.logger.error(f"Erro ao salvar configurações: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")
    
    def _search_and_send(self):
        """Busca e envia os arquivos XML"""
        # Verificar se já está processando
        if self.is_processing:
            messagebox.showwarning("Aviso", "Já existe um processamento em andamento.")
            return
        
        # Limpar status
        self.status_text.delete("0.0", "end")
        self._add_status("🔍 Validando dados do formulário...")
        
        # Obter valores dos campos
        doc_id = self.document_id_var.get().strip()
        doc_id_clean = ''.join(filter(str.isdigit, doc_id))
        
        empresa = self.company_var.get().strip()
        emails = self.email_widget.get_emails()
        periods = self.period_selector.get_periods()
        
        # Validar campos individualmente com mensagens específicas
        if not doc_id_clean:
            self._add_status("❌ ERRO: CPF/CNPJ não foi preenchido!")
            messagebox.showerror("Erro", "Por favor, preencha o CPF/CNPJ.")
            return
        
        # Validar conforme o tipo selecionado
        doc_type = self.doc_type_var.get()
        if doc_type == "CPF" and len(doc_id_clean) != 11:
            self._add_status(f"❌ ERRO: CPF inválido! Tem {len(doc_id_clean)} dígitos (deve ter 11)")
            messagebox.showerror("Erro", f"CPF inválido!\n\nCPF deve ter exatamente 11 dígitos.\n\nVocê digitou: {len(doc_id_clean)} dígitos")
            return
        
        if doc_type == "CNPJ" and len(doc_id_clean) != 14:
            self._add_status(f"❌ ERRO: CNPJ inválido! Tem {len(doc_id_clean)} dígitos (deve ter 14)")
            messagebox.showerror("Erro", f"CNPJ inválido!\n\nCNPJ deve ter exatamente 14 dígitos.\n\nVocê digitou: {len(doc_id_clean)} dígitos")
            return
        
        if not empresa:
            self._add_status("❌ ERRO: Nome da empresa não foi preenchido!")
            messagebox.showerror("Erro", "Por favor, preencha o Nome da Empresa.")
            return
        
        if not emails or len(emails) == 0:
            self._add_status("❌ ERRO: Nenhum email foi adicionado!")
            messagebox.showerror(
                "Erro", 
                "Por favor, adicione pelo menos um email!\n\n"
                "Digite o email e pressione Enter ou clique no botão +."
            )
            return
        
        if not periods or len(periods) == 0:
            self._add_status("❌ ERRO: Nenhum período foi selecionado!")
            messagebox.showerror("Erro", "Por favor, selecione pelo menos um período.")
            return
        
        # Validações OK
        self._add_status("✅ Validação concluída com sucesso!")
        self._add_status(f"📋 Empresa: {empresa}")
        self._add_status(f"📋 {doc_type}: {doc_id} ({len(doc_id_clean)} dígitos)")
        self._add_status(f"📧 Email(s): {len(emails)} destinatário(s)")
        self._add_status(f"📅 Período(s): {len(periods)} período(s)")
        self._add_status("")  # Linha em branco
        
        # Forçar atualização da interface
        self.root.update_idletasks()
        
        # Armazenar valores na configuração sem salvar no arquivo
        # (apenas para usar durante o processamento)
        self.config['document_id'] = doc_id
        self.config['document_id_clean'] = doc_id_clean
        self.config['doc_type'] = doc_type
        self.config['company_name'] = empresa
        self.config['email'] = emails[0] if emails else ''  # Salvar o primeiro email
        
        # Iniciar estado de processamento
        self._start_processing()
        
        self._add_status(f"🔎 Iniciando busca para CPF/CNPJ: {doc_id}")
        self._add_status(f"📅 Períodos selecionados: {', '.join(periods)}")
        self._add_status(f"📧 Destinatários: {', '.join(emails)}")
        self._add_status("")  # Linha em branco
        
        # Forçar atualização antes de iniciar thread
        self.root.update_idletasks()
        
        # Pequeno delay para usuário ver o feedback (300ms)
        self.root.after(300, lambda: self._start_processing_thread(doc_id_clean, emails, periods))
    
    def _start_processing_thread(self, doc_id_clean, emails, periods):
        """Inicia a thread de processamento após delay"""
        # Iniciar processamento em thread separada
        self.current_thread = threading.Thread(
            target=self._process_xml_sending_wrapper,
            args=(doc_id_clean, emails, periods)
        )
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def _start_processing(self):
        """Inicia o estado de processamento (desabilita botões, mostra loading)"""
        self.is_processing = True
        self.processing_cancelled = False
        
        # Desabilitar botão de enviar
        self.send_button.configure(state="disabled")
        
        # Mostrar botão de cancelar
        self.cancel_button.pack(side="left", padx=5)
        
        # Mostrar e iniciar barra de progresso
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.start()
    
    def _stop_processing(self):
        """Para o estado de processamento (habilita botões, esconde loading)"""
        self.is_processing = False
        self.processing_cancelled = False
        
        # Habilitar botão de enviar
        self.send_button.configure(state="normal")
        
        # Esconder botão de cancelar
        self.cancel_button.pack_forget()
        
        # Parar e esconder barra de progresso
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
    
    def _cancel_processing(self):
        """Cancela o processamento em andamento"""
        if self.is_processing:
            self.processing_cancelled = True
            self._add_status("⚠️ Cancelamento solicitado. Aguarde a conclusão da operação atual...")
            self.cancel_button.configure(state="disabled", text="Cancelando...")
    
    def _process_xml_sending_wrapper(self, doc_id, emails, periods):
        """
        Wrapper para processar o envio com tratamento de erro global.
        
        Args:
            doc_id (str): CPF/CNPJ limpo (apenas números)
            emails (list): Lista de emails de destino
            periods (list): Lista de períodos a processar
        """
        try:
            self._process_xml_sending(doc_id, emails, periods)
        except Exception as e:
            # Capturar qualquer erro não tratado
            error_msg = f"❌ ERRO CRÍTICO: {type(e).__name__}: {str(e)}"
            self._add_status(error_msg)
            self.logger.error(f"Erro crítico no processamento: {e}", exc_info=True)
            
            # Mostrar alerta para o usuário
            self.root.after(0, lambda: messagebox.showerror(
                "Erro Crítico",
                f"Ocorreu um erro durante o processamento:\n\n{str(e)}\n\nVerifique os logs para mais detalhes."
            ))
        finally:
            # Sempre parar o estado de processamento ao finalizar
            self.root.after(0, self._stop_processing)
    
    def _process_xml_sending(self, doc_id, emails, periods):
        """
        Processa o envio de arquivos XML em uma thread separada.
        
        Args:
            doc_id (str): CPF/CNPJ limpo (apenas números)
            emails (list): Lista de emails de destino
            periods (list): Lista de períodos a processar
        """
        start_time = datetime.now()
        
        # Validar configurações SMTP antes de iniciar
        smtp_config = self.config.get('smtp', {})
        if not smtp_config.get('server') or not smtp_config.get('username') or not smtp_config.get('password'):
            error_msg = (
                "❌ ERRO: Configurações de email (SMTP) não estão completas.\n"
                "Acesse o menu 'Configurações' para configurar o servidor SMTP."
            )
            self._add_status(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Erro de Configuração", error_msg))
            return
        
        try:
            xml_finder = XMLFinder(self.config.get('base_path'))
            zip_service = ZipService()
            # Inicializar EmailService com retry (3 tentativas, 5s entre cada)
            email_service = EmailService(smtp_config, max_retries=3, retry_delay=5)
        except Exception as e:
            error_msg = f"❌ ERRO ao inicializar serviços: {str(e)}"
            self._add_status(error_msg)
            self.logger.error(f"Erro ao inicializar serviços: {e}")
            return
        
        total_periods = len(periods)
        processed_periods = 0
        
        for period in periods:
            # Verificar se o processamento foi cancelado
            if self.processing_cancelled:
                self._add_status("⚠️ Processamento cancelado pelo usuário.")
                break
            
            try:
                # Formatar período para o formato esperado (AAAAMM)
                year = period.split('-')[0]
                month = period.split('-')[1]
                period_formatted = f"{year}{month}"
                
                # Converter mês numérico para nome do mês em português
                month_names = {
                    "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
                    "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
                    "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
                }
                month_name = month_names.get(month, month)
                period_display = f"{month_name} de {year}"
                
                self._add_status(f"Buscando arquivos para o período: {period_formatted}")
                
                # Buscar arquivos XML
                xml_files = xml_finder.find_xml_files(doc_id, period_formatted)
                
                nfce_files = xml_files['nfce']
                nfe_files = xml_files['nfe']
                
                self._add_status(f"Encontrados {len(nfce_files)} arquivos NFC-e e {len(nfe_files)} arquivos NF-e")
                
                # Verificar se encontrou arquivos
                total_files = len(nfce_files) + len(nfe_files)
                if total_files == 0:
                    self._add_status(f"Nenhum arquivo encontrado para o período {period}")
                    continue
                
                # CORREÇÃO PRINCIPAL: Passar o dicionário organizado para manter separação por tipo
                self._add_status(f"Compactando {total_files} arquivos organizados por tipo (NFCe e NFe em pastas separadas)...")
                
                zip_path = f"temp/{doc_id}_{period_formatted}_xmls.zip"
                os.makedirs("temp", exist_ok=True)
                
                # IMPORTANTE: Usar dicionário organizado em vez de lista simples
                files_organized = {
                    'nfce': nfce_files,  # Lista de arquivos NFCe
                    'nfe': nfe_files     # Lista de arquivos NFe
                }
                
                # Usar organize_by_type=True para criar estrutura de pastas
                compressed_path = zip_service.compress_files(
                    files_organized,      # Dicionário organizado
                    zip_path,            # Caminho do ZIP
                    organize_by_type=True # CRUCIAL: Garante organização em pastas
                )
                
                self._add_status(f"ZIP criado com estrutura organizada:")
                self._add_status(f"  - Pasta NFCe/: {len(nfce_files)} arquivo(s)")
                self._add_status(f"  - Pasta NFe/: {len(nfe_files)} arquivo(s)")
                
                # Preparar informações para o email
                company_info = {
                    'name': self.company_var.get(),
                    'document_id': self.document_id_var.get(),
                    'period': period_display
                }
                
                files_info = {
                    'nfce_count': len(nfce_files),
                    'nfe_count': len(nfe_files)
                }
                
                # Verificar novamente antes de enviar email
                if self.processing_cancelled:
                    self._add_status("⚠️ Processamento cancelado antes do envio do email.")
                    break
                
                # Enviar email com retry
                self._add_status(f"📧 Enviando para {len(emails)} destinatário(s): {', '.join(emails)}")
                
                subject = f"Arquivos XML {period_display} - {self.company_var.get()}"
                body = f"""
                Olá,
                
                Seguem os arquivos XML de NF-e e NFC-e referentes ao período {period_display}.
                
                Empresa: {self.company_var.get()}
                CNPJ: {self.document_id_var.get()}
                
                Os arquivos estão organizados em pastas separadas dentro do arquivo ZIP:
                - Pasta NFCe/: {len(nfce_files)} arquivo(s)
                - Pasta NFe/: {len(nfe_files)} arquivo(s)
                
                Este é um email automático, por favor não responda.
                """
                
                # Callback para mostrar tentativas
                def on_retry(attempt, max_attempts):
                    if attempt > 1:
                        self._add_status(f"   🔄 Tentativa {attempt}/{max_attempts}...")
                
                try:
                    # Usar send_email_with_retry (suporta múltiplos emails)
                    sucesso, tentativas, erro = email_service.send_email_with_retry(
                        emails,  # Lista de emails
                        subject, 
                        body, 
                        [compressed_path],
                        company_info=company_info,
                        files_info=files_info,
                        on_retry_callback=on_retry
                    )
                    
                    # Registrar no histórico
                    status_hist = 'sucesso' if sucesso else 'erro'
                    tempo_proc = (datetime.now() - start_time).total_seconds()
                    
                    if self.history_manager:
                        self.history_manager.add_envio(
                            documento=doc_id,
                            empresa=self.company_var.get(),
                            periodo=period,
                            destinatarios=emails,
                            nfce_count=len(nfce_files),
                            nfe_count=len(nfe_files),
                            status=status_hist,
                            tentativas=tentativas,
                            erro=erro,
                            arquivo_zip=compressed_path,
                            tempo_processamento=tempo_proc
                        )
                    
                    if sucesso:
                        processed_periods += 1
                        self._add_status(f"✅ Envio concluído com sucesso! ({processed_periods}/{total_periods})")
                        if tentativas > 1:
                            self._add_status(f"   ℹ️ Sucesso após {tentativas} tentativa(s)")
                        self._add_status(f"📦 Arquivo enviado com estrutura organizada:")
                        self._add_status(f"   📁 NFCe/ ({len(nfce_files)} arquivos)")
                        self._add_status(f"   📁 NFe/ ({len(nfe_files)} arquivos)")
                    else:
                        self._add_status(f"❌ ERRO: Falha após {tentativas} tentativa(s)")
                        if erro:
                            self._add_status(f"   {erro}")
                        
                except Exception as email_error:
                    error_details = str(email_error)
                    self._add_status(f"❌ ERRO INESPERADO ao enviar email:")
                    self._add_status(f"   {error_details}")
                    self.logger.error(f"Erro no envio de email: {email_error}", exc_info=True)
                    
                    # Registrar erro no histórico
                    if self.history_manager:
                        tempo_proc = (datetime.now() - start_time).total_seconds()
                        self.history_manager.add_envio(
                            documento=doc_id,
                            empresa=self.company_var.get(),
                            periodo=period,
                            destinatarios=emails,
                            nfce_count=len(nfce_files),
                            nfe_count=len(nfe_files),
                            status='erro',
                            tentativas=1,
                            erro=error_details,
                            tempo_processamento=tempo_proc
                        )
                    
                    # Mostrar alerta de erro específico
                    self.root.after(0, lambda msg=error_details: messagebox.showerror(
                        "Erro no Envio de Email",
                        f"Falha ao enviar email:\n\n{msg}\n\nVerifique as configurações de SMTP e sua conexão com a internet."
                    ))
                
                # Limpar arquivos temporários
                try:
                    if os.path.exists(compressed_path):
                        os.remove(compressed_path)
                        self._add_status("🧹 Arquivos temporários removidos.")
                except Exception as cleanup_error:
                    self.logger.warning(f"Erro ao remover arquivo temporário: {cleanup_error}")
                
            except Exception as e:
                self._add_status(f"❌ ERRO durante o processamento do período {period}:")
                self._add_status(f"   {type(e).__name__}: {str(e)}")
                self.logger.error(f"Erro no processamento do período {period}: {e}", exc_info=True)
                
                # Perguntar se deseja continuar com os próximos períodos
                if len(periods) > 1 and periods.index(period) < len(periods) - 1:
                    continue_processing = True  # Por padrão, continua
                    self._add_status(f"   Continuando com o próximo período...")
        
        # Mensagem final
        if self.processing_cancelled:
            self._add_status("⚠️ Processamento cancelado.")
        elif processed_periods == total_periods:
            self._add_status(f"🎉 Processamento concluído com sucesso! {processed_periods}/{total_periods} períodos enviados.")
        elif processed_periods > 0:
            self._add_status(f"⚠️ Processamento concluído com erros. {processed_periods}/{total_periods} períodos enviados com sucesso.")
        else:
            self._add_status(f"❌ Nenhum período foi processado com sucesso.")
    
    def _add_status(self, message):
        """
        Adiciona uma mensagem à área de status.
        
        Args:
            message (str): Mensagem a ser adicionada
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert("end", f"[{timestamp}] {message}\n")
        self.status_text.see("end")
        self.root.update()
    
    def _clear_status(self):
        """Limpa todos os logs da área de status"""
        self.status_text.delete("1.0", "end")
        self._add_status("✅ Logs limpos")
    
    def _check_for_updates(self):
        """Verifica se há atualizações disponíveis"""
        from modules.update_checker import UpdateChecker
        from gui.update_window import UpdateWindow
        import threading
        
        def check_in_thread():
            # Criar verificador
            # IMPORTANTE: Altere 'repo_owner' e 'repo_name' para seu repositório GitHub
            checker = UpdateChecker(
                repo_owner="adrielteles",  # ← ALTERAR para seu usuário do GitHub
                repo_name="sender_xml_new_version",  # ← ALTERAR para nome do seu repositório
                current_version=self.app_version
            )
            
            # Verificar atualizações
            result = checker.check_for_updates()
            
            # Atualizar na thread principal (UI)
            self.root.after(0, lambda: self._show_update_result(result, checker))
        
        # Mostrar loading
        self._add_status("🔄 Verificando atualizações...")
        
        # Executar em thread separada
        thread = threading.Thread(target=check_in_thread, daemon=True)
        thread.start()
    
    def _show_update_result(self, result, checker):
        """
        Mostra o resultado da verificação de atualização.
        
        Args:
            result (dict): Resultado da verificação
            checker (UpdateChecker): Instância do verificador
        """
        if result.get('error'):
            messagebox.showwarning(
                "Verificação de Atualizações",
                f"Não foi possível verificar atualizações:\n\n{result['error']}"
            )
            self._add_status("❌ Falha ao verificar atualizações")
            return
        
        if result['has_update']:
            # Importar aqui para evitar import circular
            from gui.update_window import UpdateWindow
            
            # Abrir janela de atualização
            update_window = UpdateWindow(self.root, result)
            update_window.on_download = checker.download_update
            self._add_status(f"✅ Nova versão disponível: {result['latest_version']}")
        else:
            messagebox.showinfo(
                "Verificação de Atualizações",
                f"Você está usando a versão mais recente!\n\nVersão: {result['latest_version']}"
            )
            self._add_status("✅ Aplicação está atualizada")