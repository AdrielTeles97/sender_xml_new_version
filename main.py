#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import tempfile
import zipfile
from datetime import datetime

# Use CustomTkinter para interface moderna
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox

# Módulos da aplicação
from modules.config_manager import ConfigManager
from gui.main_window import MainWindow

class XMLSenderApp:
    """Aplicação principal para envio de arquivos XML"""
    
    def __init__(self):
        self.app_version = "1.0.0"
        self.app_name = "Envio de Arquivos XML"
        self.developer = "Adriel Teles"
        
        # Configurar logging
        self._setup_logging()
        
        # Carregar configurações
        self.config_manager = ConfigManager('config/settings.json')
        self.config = self.config_manager.load_config()
        
        # Configurar a interface gráfica
        self._setup_gui()
    
    def _setup_logging(self):
        """Configuração do sistema de logs"""
        os.makedirs('logs', exist_ok=True)
        
        # Configuração básica do logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/app.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Logger específico da aplicação
        self.logger = logging.getLogger("XMLSender")
        self.logger.info(f"Iniciando aplicação {self.app_name} v{self.app_version}")
    
    def _setup_gui(self):
        """Configuração da interface gráfica"""
        # Definir tema da aplicação
        ctk.set_appearance_mode("dark")  # Modos: "dark", "light", "system"
        ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"
        
        # Criar janela principal
        self.root = ctk.CTk()
        self.root.title(f"{self.app_name} - v{self.app_version}")
        self.root.geometry("800x700")
        self.root.minsize(800, 700)
        
        # Definir ícone da aplicação
        self._setup_icon()
        
        # Inicializar a janela principal com todos os componentes
        self.main_window = MainWindow(
            self.root, 
            self.config, 
            self.config_manager,
            self.app_version,
            self.developer,
            self.on_exit,
        )
        
        # Configurar ação ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
    
    def _setup_icon(self):
        """Configuração do ícone da aplicação"""
        try:
            icon_paths = [
                "assets/icon.png",
                "assets/icon.ico",
                "icon.png",
                "icon.ico"
            ]
            
            icon_loaded = False
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    try:
                        if icon_path.endswith('.png'):
                            icon_img = Image.open(icon_path)
                            icon_photo = ImageTk.PhotoImage(icon_img)
                            self.root.iconphoto(True, icon_photo)
                        elif icon_path.endswith('.ico'):
                            self.root.iconbitmap(icon_path)
                        
                        self.logger.info(f"Ícone da aplicação carregado: {icon_path}")
                        icon_loaded = True
                        break
                    except Exception as e:
                        self.logger.warning(f"Erro ao carregar ícone {icon_path}: {e}")
                        continue
            
            if not icon_loaded:
                self.logger.warning("Nenhum ícone foi carregado")
                
        except Exception as e:
            self.logger.warning(f"Erro geral ao configurar ícone: {e}")
    
    def _create_directories(self):
        """Criar diretórios necessários para a aplicação"""
        directories = [
            'logs',
            'config',
            'temp',
            'assets'
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                self.logger.debug(f"Diretório verificado/criado: {directory}")
            except Exception as e:
                self.logger.error(f"Erro ao criar diretório {directory}: {e}")
    
    def _validate_dependencies(self):
        """Validar se todas as dependências estão disponíveis"""
        required_modules = [
            'customtkinter',
            'PIL',
            'smtplib',
            'email',
            'zipfile',
            'xml.etree.ElementTree'
        ]
        
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
                self.logger.debug(f"Módulo disponível: {module}")
            except ImportError:
                missing_modules.append(module)
                self.logger.error(f"Módulo não encontrado: {module}")
        
        if missing_modules:
            error_msg = f"Módulos não encontrados: {', '.join(missing_modules)}"
            self.logger.error(error_msg)
            messagebox.showerror("Erro de Dependências", error_msg)
            return False
        
        return True
    
    def _load_default_config(self):
        """Carregar configurações padrão se necessário"""
        default_config = {
            'document_id': '',
            'company_name': '',
            'email': '',
            'base_path': 'C:\\XMLs',
            'smtp': {
                'server': 'smtp.gmail.com',
                'port': 587,
                'username': '',
                'password': '',
                'use_tls': True
            },
            'ui': {
                'theme': 'dark',
                'color_theme': 'blue'
            }
        }
        
        # Atualizar configurações com valores padrão se não existirem
        for key, value in default_config.items():
            if key not in self.config:
                self.config[key] = value
                self.logger.info(f"Configuração padrão adicionada: {key}")
    
    def on_exit(self):
        """Ação ao fechar a aplicação"""
        self.logger.info("Iniciando processo de encerramento da aplicação")
        
        try:
            # Salvar configurações atuais
            if hasattr(self, 'main_window'):
                # Salvar dados do formulário
                self.config['document_id'] = self.main_window.document_id_var.get()
                self.config['company_name'] = self.main_window.company_var.get()
                self.config['email'] = self.main_window.email_var.get()
            
            # Salvar configurações no arquivo
            self.config_manager.save_config(self.config)
            self.logger.info("Configurações salvas com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar configurações: {e}")
        
        try:
            # Limpar arquivos temporários
            temp_dir = "temp"
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        self.logger.debug(f"Arquivo temporário removido: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Erro ao limpar arquivos temporários: {e}")
        
        self.logger.info("Aplicação encerrada")
        self.root.destroy()
    
    def run(self):
        """Iniciar a aplicação"""
        try:
            # Criar diretórios necessários
            self._create_directories()
            
            # Validar dependências
            if not self._validate_dependencies():
                return
            
            # Carregar configurações padrão
            self._load_default_config()
            
            self.logger.info("Aplicação iniciada com sucesso")
            self.root.mainloop()
            
        except Exception as e:
            self.logger.error(f"Erro crítico na aplicação: {e}")
            messagebox.showerror(
                "Erro Crítico", 
                f"Ocorreu um erro crítico na aplicação:\n\n{str(e)}\n\nVerifique os logs para mais detalhes."
            )

def main():
    """Função principal da aplicação"""
    try:
        app = XMLSenderApp()
        app.run()
    except KeyboardInterrupt:
        print("\nAplicação interrompida pelo usuário")
    except Exception as e:
        print(f"Erro fatal: {e}")
        logging.error(f"Erro fatal: {e}")

if __name__ == "__main__":
    main()