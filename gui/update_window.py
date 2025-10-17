#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import customtkinter as ctk
from tkinter import messagebox

class UpdateWindow(ctk.CTkToplevel):
    """Janela de notificação de atualização"""
    
    def __init__(self, parent, update_info):
        """
        Inicializa a janela de atualização.
        
        Args:
            parent: Janela pai
            update_info (dict): Informações da atualização
        """
        super().__init__(parent)
        
        self.update_info = update_info
        self.on_download = None  # Callback para download
        
        # Configurar janela
        self.title("Atualização Disponível")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Centralizar na tela
        self.update()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"+{x}+{y}")
        
        # Manter janela no topo
        self.attributes('-topmost', True)
        
        self._build_interface()
    
    def _build_interface(self):
        """Constrói a interface da janela"""
        # Ícone e título
        header_frame = ctk.CTkFrame(self, fg_color=("gray85", "gray20"))
        header_frame.pack(fill="x", padx=0, pady=0)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="🎉 Nova Versão Disponível!",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header_label.pack(pady=20)
        
        # Informações da versão
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        version_label = ctk.CTkLabel(
            info_frame,
            text=f"Versão {self.update_info['latest_version']} está disponível",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        version_label.pack(pady=(10, 5))
        
        # Notas de lançamento
        notes_label = ctk.CTkLabel(
            info_frame,
            text="Novidades:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        notes_label.pack(fill="x", padx=10, pady=(10, 5))
        
        notes_text = ctk.CTkTextbox(
            info_frame,
            height=150,
            wrap="word",
            font=ctk.CTkFont(size=11)
        )
        notes_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Inserir notas de lançamento
        release_notes = self.update_info.get('release_notes', 'Nenhuma descrição disponível.')
        notes_text.insert("1.0", release_notes)
        notes_text.configure(state="disabled")
        
        # Botões
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        download_btn = ctk.CTkButton(
            button_frame,
            text="📥 Baixar Atualização",
            command=self._on_download_clicked,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        download_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        later_btn = ctk.CTkButton(
            button_frame,
            text="Mais Tarde",
            command=self.destroy,
            height=40,
            fg_color="gray50",
            hover_color="gray60",
            font=ctk.CTkFont(size=13)
        )
        later_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    def _on_download_clicked(self):
        """Callback do botão de download"""
        if self.on_download:
            self.on_download(self.update_info['download_url'])
        self.destroy()

