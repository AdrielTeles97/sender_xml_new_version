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
from gui.settings_window import SettingsWindow
from gui.period_selector import PeriodSelector

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
        
        # Definir tamanho mínimo da janela para garantir que todos os elementos sejam visíveis
        self.root.minsize(600, 950)
        
        # Construir interface
        self._build_interface()
    
    def _build_interface(self):
        """Constrói a interface da janela principal"""
        # Criar menu estilo Windows
        self._create_menu()
        
        # Frame principal com scrollbar para telas pequenas
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True)
        
        # Frame principal com padding adequado
        main_frame = ctk.CTkFrame(main_container)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        header_title = ctk.CTkLabel(
            header_frame,
            text="Envio de Arquivos XML",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header_title.pack(pady=10)
        
        # Frame do formulário
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Adicionar padding interno para melhor visualização
        form_inner = ctk.CTkFrame(form_frame)
        form_inner.pack(fill="x", expand=True, padx=10, pady=10)
        
        # CPF/CNPJ
        doc_id_label = ctk.CTkLabel(form_inner, text="CPF/CNPJ:", anchor="e", width=120)
        doc_id_label.grid(row=0, column=0, sticky="e", padx=(10, 5), pady=10)
        doc_id_entry = ctk.CTkEntry(form_inner, textvariable=self.document_id_var, width=300)
        doc_id_entry.grid(row=0, column=1, sticky="w", padx=5, pady=10)
        doc_id_entry.bind("<KeyRelease>", self._format_document_id)
        
        # Nome da Empresa
        company_label = ctk.CTkLabel(form_inner, text="Nome da Empresa:", anchor="e", width=120)
        company_label.grid(row=1, column=0, sticky="e", padx=(10, 5), pady=10)
        company_entry = ctk.CTkEntry(form_inner, textvariable=self.company_var, width=300)
        company_entry.grid(row=1, column=1, sticky="w", padx=5, pady=10)
        
        # Email
        email_label = ctk.CTkLabel(form_inner, text="Email:", anchor="e", width=120)
        email_label.grid(row=2, column=0, sticky="e", padx=(10, 5), pady=10)
        email_entry = ctk.CTkEntry(form_inner, textvariable=self.email_var, width=300)
        email_entry.grid(row=2, column=1, sticky="w", padx=5, pady=10)
        
        # Período (usando o componente PeriodSelector)
        period_label = ctk.CTkLabel(form_inner, text="Período(s):", anchor="e", width=120)
        period_label.grid(row=3, column=0, sticky="ne", padx=(10, 5), pady=10)
        
        # Frame para o componente do seletor de período para controlar o tamanho
        period_container = ctk.CTkFrame(form_inner, fg_color="transparent")
        period_container.grid(row=3, column=1, sticky="ew", padx=5, pady=10)
        
        self.period_selector = PeriodSelector(period_container)
        self.period_selector.pack(fill="x", expand=True)
        
        # Auto-salvar configurações ao preencher campos
        doc_id_entry.bind("<FocusOut>", lambda e: self._save_settings(False))
        company_entry.bind("<FocusOut>", lambda e: self._save_settings(False))
        email_entry.bind("<FocusOut>", lambda e: self._save_settings(False))
        
        # Ajustar o grid
        form_inner.grid_columnconfigure(0, weight=1)
        form_inner.grid_columnconfigure(1, weight=3)
        
        # Botão de busca e envio
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=15)
        
        send_button = ctk.CTkButton(
            button_frame,
            text="Buscar e Enviar",
            command=self._search_and_send,
            width=200,
            height=40
        )
        send_button.pack()
        
        # Status - Com altura fixa mínima para garantir visibilidade
        status_label_frame = ctk.CTkFrame(main_frame)
        status_label_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        status_label = ctk.CTkLabel(status_label_frame, text="Status:", anchor="w")
        status_label.pack(anchor="w", padx=10, pady=5)
        
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.status_text = ctk.CTkTextbox(status_frame)
        self.status_text.pack(fill="both", expand=True, padx=5, pady=5)
        # Definir altura mínima para o campo de status
        self.status_text.configure(height=150)
        
        # Rodapé
        footer_frame = ctk.CTkFrame(main_frame, height=30)
        footer_frame.pack(fill="x", side="bottom", pady=5)
        
        version_label = ctk.CTkLabel(
            footer_frame,
            text=f"v{self.app_version}",
            font=ctk.CTkFont(size=10)
        )
        version_label.pack(side="left", padx=10)
        
        developer_label = ctk.CTkLabel(
            footer_frame,
            text=f"Desenvolvido por: {self.developer} © {datetime.now().year}",
            font=ctk.CTkFont(size=10)
        )
        developer_label.pack(side="right", padx=10)

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
        
        # Menu Configurações
        menubar.add_command(label="Configurações", command=self._show_settings)
        
        # Menu Ajuda
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Ajuda", command=self._show_help)
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
    
    def _format_document_id(self, event=None):
        """Formata automaticamente o CPF/CNPJ com máscara"""
        current = self.document_id_var.get().replace(".", "").replace("/", "").replace("-", "")
        current = ''.join(filter(str.isdigit, current))
        
        # Se parece um CPF (11 dígitos)
        if len(current) <= 11:
            formatted = current
            if len(current) > 3:
                formatted = f"{current[:3]}.{current[3:]}"
            if len(current) > 6:
                formatted = f"{formatted[:7]}.{current[6:]}"
            if len(current) > 9:
                formatted = f"{formatted[:11]}-{current[9:]}"
        # Se parece um CNPJ (14 dígitos)
        else:
            formatted = current
            if len(current) > 2:
                formatted = f"{current[:2]}.{current[2:]}"
            if len(current) > 5:
                formatted = f"{formatted[:6]}.{current[5:]}"
            if len(current) > 8:
                formatted = f"{formatted[:10]}.{current[8:]}"
            if len(current) > 12:
                formatted = f"{formatted[:15]}/{current[12:]}"
            if len(current) > 14:
                formatted = f"{formatted[:18]}-{current[14:]}"
        
        # Limitar ao tamanho máximo (18 para CNPJ com máscara)
        if len(formatted) > 18:
            formatted = formatted[:18]
        
        # Atualizar o campo se o valor formatado for diferente
        if formatted != self.document_id_var.get():
            self.document_id_var.set(formatted)
    
    def _show_settings(self):
        """Exibe a janela de configurações"""
        settings_window = SettingsWindow(self.root, self.config, self.config_manager)
    
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
        # Limpar status
        self.status_text.delete("0.0", "end")
        
        # Obter valores dos campos
        doc_id = self.document_id_var.get().strip()
        doc_id_clean = ''.join(filter(str.isdigit, doc_id))
        
        email = self.email_var.get().strip()
        periods = self.period_selector.get_periods()
        
        # Validar campos
        if not doc_id_clean or not email or not periods:
            messagebox.showerror("Erro", "CPF/CNPJ, email e pelo menos um período são obrigatórios.")
            return
        
        # Armazenar valores na configuração sem salvar no arquivo
        # (apenas para usar durante o processamento)
        self.config['document_id'] = doc_id
        self.config['document_id_clean'] = doc_id_clean
        self.config['company_name'] = self.company_var.get().strip()
        self.config['email'] = email
        
        self._add_status(f"Iniciando busca para CPF/CNPJ: {doc_id}")
        self._add_status(f"Períodos selecionados: {', '.join(periods)}")
        
        # Iniciar processamento em thread separada
        thread = threading.Thread(
            target=self._process_xml_sending,
            args=(doc_id_clean, email, periods)
        )
        thread.daemon = True
        thread.start()
    
    def _process_xml_sending(self, doc_id, email, periods):
        """
        Processa o envio de arquivos XML em uma thread separada.
        
        Args:
            doc_id (str): CPF/CNPJ limpo (apenas números)
            email (str): Email de destino
            periods (list): Lista de períodos a processar
        """
        xml_finder = XMLFinder(self.config.get('base_path'))
        zip_service = ZipService()
        email_service = EmailService(self.config.get('smtp', {}))
        
        for period in periods:
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
                
                # Enviar email
                self._add_status(f"Enviando email para {email}...")
                
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
                
                result = email_service.send_email(
                    email, 
                    subject, 
                    body, 
                    [compressed_path],
                    company_info=company_info,
                    files_info=files_info
                )
                
                if result:
                    self._add_status(f"✅ Envio concluído com sucesso para o período {period}!")
                    self._add_status(f"📦 Arquivo enviado com estrutura organizada:")
                    self._add_status(f"   📁 NFCe/ ({len(nfce_files)} arquivos)")
                    self._add_status(f"   📁 NFe/ ({len(nfe_files)} arquivos)")
                else:
                    self._add_status(f"❌ ERRO: Falha no envio dos arquivos para o período {period}.")
                
                # Limpar arquivos temporários
                if os.path.exists(compressed_path):
                    os.remove(compressed_path)
                    self._add_status("🧹 Arquivos temporários removidos.")
                
            except Exception as e:
                self._add_status(f"❌ ERRO durante o processamento do período {period}: {str(e)}")
                self.logger.error(f"Erro no processamento do período {period}: {e}")
        
        self._add_status("🎉 Processamento concluído!")
    
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