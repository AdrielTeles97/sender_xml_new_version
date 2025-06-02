#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
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
        
        logging.basicConfig(
            filename='logs/app.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Adicionar log para o console também para facilitar a depuração
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        
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
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Definir ícone da aplicação
        try:
            if os.path.exists("assets/icon.png"):
                icon_img = Image.open("assets/icon.png")
                icon_photo = ImageTk.PhotoImage(icon_img)
                self.root.iconphoto(True, icon_photo)
                self.logger.info("Ícone da aplicação carregado com sucesso")
            else:
                self.logger.warning("Arquivo de ícone não encontrado: assets/icon.png")
        except Exception as e:
            self.logger.warning(f"Erro ao carregar ícone: {e}")
        
        
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
    
    def on_exit(self):
        """Ação ao fechar a aplicação"""
        self.logger.info("Encerrando aplicação")
        try:
            # Salvar configurações antes de sair
            self.config_manager.save_config(self.config)
        except Exception as e:
            self.logger.error(f"Erro ao salvar configurações: {e}")
        
        self.root.destroy()
    
    def run(self):
        """Iniciar a aplicação"""
        self.logger.info("Aplicação iniciada")
        self.root.mainloop()

if __name__ == "__main__":
    app = XMLSenderApp()
    app.run()