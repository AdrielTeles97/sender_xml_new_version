#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tkinter import messagebox, Toplevel, Frame

import customtkinter as ctk

from modules.email_service import EmailService

class SettingsWindow:
    """Janela de configurações da aplicação"""
    
    def __init__(self, parent, config, config_manager):
        """
        Inicializa a janela de configurações.
        
        Args:
            parent (CTk): Janela pai
            config (dict): Configurações da aplicação
            config_manager (ConfigManager): Gerenciador de configurações
        """
        self.parent = parent
        self.config = config
        self.config_manager = config_manager
        
        self.logger = logging.getLogger("XMLSender.SettingsWindow")
        
        # Criar janela
        self.window = Toplevel(parent)
        self.window.title("Configurações")
        self.window.geometry("600x650")
        self.window.transient(parent)  # Define a janela como filha da janela principal
        self.window.grab_set()  # Bloqueia a janela principal até que essa seja fechada
        
        # Centralizar a janela em relação à janela pai
        x = parent.winfo_x() + (parent.winfo_width() / 2) - (600 / 2)
        y = parent.winfo_y() + (parent.winfo_height() / 2) - (550 / 2)
        self.window.geometry("+%d+%d" % (x, y))
        
        # Configurar a interface
        self._build_interface()
        
        # Carregar configurações
        self._load_settings()
        
        # Exibir a aba SMTP por padrão
        self._show_tab("smtp")
    
    def _build_interface(self):
        """Constrói a interface da janela de configurações"""
        # Container principal para toda a interface
        main_container = Frame(self.window)
        main_container.pack(fill="both", expand=True)
        
        # Frame principal - cria um frame customtkinter dentro do frame tkinter padrão
        self.main_frame = ctk.CTkFrame(main_container)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Configurações do Sistema",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame para abas (botões)
        tabs_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        tabs_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botões de aba - usando segmentedbutton para melhor estética
        self.tab_var = ctk.StringVar(value="smtp")
        self.tab_buttons = ctk.CTkSegmentedButton(
            tabs_frame,
            values=["SMTP", "Diretórios"],
            command=self._on_tab_change,
            variable=self.tab_var
        )
        self.tab_buttons.pack(padx=10)
        
        # Container para conteúdo das abas
        self.tabs_container = ctk.CTkFrame(self.main_frame)
        self.tabs_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frames para cada aba (inicialmente invisíveis)
        self.smtp_frame = ctk.CTkFrame(self.tabs_container)
        self.directories_frame = ctk.CTkFrame(self.tabs_container)
        
        # Construir o conteúdo das abas
        self._build_smtp_tab(self.smtp_frame)
        self._build_directories_tab(self.directories_frame)
        
        # Container para botões de ação (sempre visível, fora das abas)
        # Como um frame separado no final da janela
        self.action_buttons_frame = ctk.CTkFrame(main_container)
        self.action_buttons_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        
        # Botões de ação no frame separado
        save_button = ctk.CTkButton(
            self.action_buttons_frame,
            text="Salvar",
            command=self._save_settings,
            width=100
        )
        save_button.pack(side="left", padx=10, pady=10)
        
        test_smtp_button = ctk.CTkButton(
            self.action_buttons_frame,
            text="Testar SMTP",
            command=self._test_smtp,
            width=100
        )
        test_smtp_button.pack(side="left", padx=10, pady=10)
        
        close_button = ctk.CTkButton(
            self.action_buttons_frame,
            text="Fechar",
            command=self.window.destroy,
            width=100
        )
        close_button.pack(side="right", padx=10, pady=10)
    
    def _on_tab_change(self, value):
        """
        Callback para a mudança de aba.
        
        Args:
            value (str): Valor selecionado no segmentedbutton 
        """
        if value == "SMTP":
            self._show_tab("smtp")
        elif value == "Diretórios":
            self._show_tab("directories")
    
    def _show_tab(self, tab_name):
        """
        Exibe a aba selecionada e oculta as outras.
        
        Args:
            tab_name (str): Nome da aba a ser exibida ('smtp' ou 'directories')
        """
        # Ocultar todas as abas
        self.smtp_frame.pack_forget()
        self.directories_frame.pack_forget()
        
        # Mostrar a aba selecionada
        if tab_name == "smtp":
            self.smtp_frame.pack(fill="both", expand=True)
            self.tab_var.set("SMTP")
        elif tab_name == "directories":
            self.directories_frame.pack(fill="both", expand=True)
            self.tab_var.set("Diretórios")
    
    def _build_smtp_tab(self, parent):
        """
        Constrói a aba de configurações SMTP.
        
        Args:
            parent (CTkFrame): Frame pai
        """
        # Frame de configurações SMTP
        smtp_frame = ctk.CTkFrame(parent)
        smtp_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Servidor SMTP
        server_label = ctk.CTkLabel(smtp_frame, text="Servidor SMTP:")
        server_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.smtp_server_entry = ctk.CTkEntry(smtp_frame, width=300)
        self.smtp_server_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        # Porta
        port_label = ctk.CTkLabel(smtp_frame, text="Porta:")
        port_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.smtp_port_entry = ctk.CTkEntry(smtp_frame, width=100)
        self.smtp_port_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        
        # Usuário
        username_label = ctk.CTkLabel(smtp_frame, text="Usuário:")
        username_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.smtp_username_entry = ctk.CTkEntry(smtp_frame, width=300)
        self.smtp_username_entry.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
        # Senha
        password_label = ctk.CTkLabel(smtp_frame, text="Senha:")
        password_label.grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.smtp_password_entry = ctk.CTkEntry(smtp_frame, width=300, show="*")
        self.smtp_password_entry.grid(row=3, column=1, sticky="w", padx=10, pady=10)
        
        # SSL
        self.smtp_ssl_var = ctk.BooleanVar()
        ssl_checkbox = ctk.CTkCheckBox(
            smtp_frame,
            text="Usar SSL",
            variable=self.smtp_ssl_var
        )
        ssl_checkbox.grid(row=4, column=1, sticky="w", padx=10, pady=10)
        
        # Informações sobre configuração para Gmail
        info_label = ctk.CTkLabel(
            smtp_frame,
            text="Para Gmail:\n"
                 "Servidor: smtp.gmail.com\n"
                 "Porta: 587 (TLS) ou 465 (SSL)\n"
                 "Para usar sua conta Gmail, você precisa gerar uma senha de aplicativo\n"
                 "nas configurações de segurança da conta Google.",
            justify="left"
        )
        info_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=20)
        
        # Configurar grid
        smtp_frame.grid_columnconfigure(0, weight=1)
        smtp_frame.grid_columnconfigure(1, weight=3)
    
    def _build_directories_tab(self, parent):
        """
        Constrói a aba de configurações de diretórios.
        
        Args:
            parent (CTkFrame): Frame pai
        """
        # Frame de configurações de diretórios
        dir_frame = ctk.CTkFrame(parent)
        dir_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Diretório base
        base_path_label = ctk.CTkLabel(dir_frame, text="Diretório Base:")
        base_path_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.base_path_entry = ctk.CTkEntry(dir_frame, width=300)
        self.base_path_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        browse_button = ctk.CTkButton(
            dir_frame,
            text="...",
            width=30,
            command=self._browse_directory
        )
        browse_button.grid(row=0, column=2, padx=5, pady=10)
        
        # Informações
        info_label = ctk.CTkLabel(
            dir_frame,
            text="O diretório base é o caminho onde os arquivos XML estão armazenados.\n"
                 "O sistema irá procurar os documentos no seguinte formato:\n\n"
                 "{Diretório Base}\\{CPF/CNPJ}\\Enviado\\NFCe\\{AAAAMM}\\Autorizados\n"
                 "{Diretório Base}\\{CPF/CNPJ}\\Enviado\\NF-e\\{AAAAMM}\\Autorizados",
            justify="left"
        )
        info_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=20)
        
        # Configurar grid
        dir_frame.grid_columnconfigure(0, weight=1)
        dir_frame.grid_columnconfigure(1, weight=3)
    
    def _browse_directory(self):
        """Abre diálogo para selecionar diretório"""
        from tkinter import filedialog
        directory = filedialog.askdirectory(
            title="Selecione o diretório base",
            initialdir=self.base_path_entry.get() or "C:\\"
        )
        
        if directory:
            self.base_path_entry.delete(0, "end")
            self.base_path_entry.insert(0, directory)
    
    def _load_settings(self):
        """Carrega as configurações nos campos"""
        # Configurações SMTP
        smtp_config = self.config.get('smtp', {})
        self.smtp_server_entry.insert(0, smtp_config.get('server', ''))
        self.smtp_port_entry.insert(0, str(smtp_config.get('port', 587)))
        self.smtp_username_entry.insert(0, smtp_config.get('username', ''))
        self.smtp_password_entry.insert(0, smtp_config.get('password', ''))
        self.smtp_ssl_var.set(smtp_config.get('use_ssl', False))
        
        # Configurações de diretórios
        self.base_path_entry.insert(0, self.config.get('base_path', 'C:\\DigiSat\\SuiteG6\\Servidor\\DFe'))
    
    def _save_settings(self):
        """Salva as configurações"""
        try:
            # Configurações SMTP
            self.config['smtp'] = {
                'server': self.smtp_server_entry.get().strip(),
                'port': int(self.smtp_port_entry.get().strip() or 587),
                'username': self.smtp_username_entry.get().strip(),
                'password': self.smtp_password_entry.get().strip(),
                'use_ssl': self.smtp_ssl_var.get()
            }
            
            # Configurações de diretórios
            self.config['base_path'] = self.base_path_entry.get().strip()
            
            # Salvar configurações
            self.config_manager.save_config(self.config)
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        
        except Exception as e:
            self.logger.error(f"Erro ao salvar configurações: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")
    
    def _test_smtp(self):
        """Testa a conexão SMTP"""
        # Obter configurações atuais
        smtp_config = {
            'server': self.smtp_server_entry.get().strip(),
            'port': int(self.smtp_port_entry.get().strip() or 587),
            'username': self.smtp_username_entry.get().strip(),
            'password': self.smtp_password_entry.get().strip(),
            'use_ssl': self.smtp_ssl_var.get()
        }
        
        # Validar campos
        if not smtp_config['server'] or not smtp_config['username'] or not smtp_config['password']:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios: servidor, usuário e senha.")
            return
        
        # Testar conexão
        try:
            email_service = EmailService(smtp_config)
            result = email_service.test_connection()
            
            if result:
                messagebox.showinfo("Sucesso", "Conexão SMTP realizada com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha na conexão SMTP.")
        
        except Exception as e:
            self.logger.error(f"Erro ao testar conexão SMTP: {e}")
            messagebox.showerror("Erro", f"Erro ao testar conexão SMTP: {e}")