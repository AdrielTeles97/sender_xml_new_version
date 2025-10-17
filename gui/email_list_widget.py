#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import customtkinter as ctk
import re

class EmailListWidget(ctk.CTkFrame):
    """Widget para gerenciar lista de múltiplos emails com chips/tags"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.emails = []
        
        # Frame principal
        self.configure(fg_color=("gray90", "gray13"))
        
        # Frame para o campo de entrada
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=5, pady=5)
        
        # Campo de entrada de email
        self.email_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Digite um email e pressione Enter",
            width=300
        )
        self.email_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.email_entry.bind("<Return>", self._on_enter_pressed)
        
        # Botão adicionar
        add_button = ctk.CTkButton(
            input_frame,
            text="+",
            width=30,
            command=self._add_email_from_entry
        )
        add_button.pack(side="left")
        
        # Frame rolável para os chips de email
        self.chips_frame = ctk.CTkScrollableFrame(
            self,
            height=100,
            fg_color=("gray85", "gray20")
        )
        self.chips_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        # Label de instruções
        self.instruction_label = ctk.CTkLabel(
            self.chips_frame,
            text="Nenhum email adicionado",
            text_color="gray"
        )
        self.instruction_label.pack(pady=10)
    
    def _on_enter_pressed(self, event):
        """Callback quando Enter é pressionado"""
        self._add_email_from_entry()
    
    def _add_email_from_entry(self):
        """Adiciona o email do campo de entrada"""
        email = self.email_entry.get().strip()
        if email:
            self.add_email(email)
            self.email_entry.delete(0, 'end')
    
    def add_email(self, email):
        """
        Adiciona um email à lista.
        
        Args:
            email (str): Endereço de email
            
        Returns:
            bool: True se adicionado com sucesso, False se inválido ou duplicado
        """
        email = email.strip().lower()
        
        # Validar formato de email
        if not self._is_valid_email(email):
            return False
        
        # Verificar duplicação
        if email in self.emails:
            return False
        
        # Adicionar à lista
        self.emails.append(email)
        
        # Esconder label de instruções se tiver emails
        if self.instruction_label.winfo_exists():
            self.instruction_label.pack_forget()
        
        # Criar chip visual
        self._create_email_chip(email)
        
        return True
    
    def _is_valid_email(self, email):
        """
        Valida formato de email.
        
        Args:
            email (str): Email a validar
            
        Returns:
            bool: True se válido
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _create_email_chip(self, email):
        """
        Cria um chip visual para o email.
        
        Args:
            email (str): Endereço de email
        """
        chip_frame = ctk.CTkFrame(
            self.chips_frame,
            fg_color=("#3B8ED0", "#1F6AA5"),
            corner_radius=15
        )
        chip_frame.pack(side="top", anchor="w", padx=3, pady=3, fill="x")
        
        # Label do email
        email_label = ctk.CTkLabel(
            chip_frame,
            text=email,
            text_color="white",
            font=("Helvetica", 11)
        )
        email_label.pack(side="left", padx=(10, 5), pady=5)
        
        # Botão remover
        remove_button = ctk.CTkButton(
            chip_frame,
            text="✕",
            width=20,
            height=20,
            fg_color="transparent",
            hover_color=("#D32F2F", "#B71C1C"),
            text_color="white",
            font=("Helvetica", 10, "bold"),
            command=lambda e=email, f=chip_frame: self._remove_email(e, f)
        )
        remove_button.pack(side="left", padx=(0, 5), pady=5)
    
    def _remove_email(self, email, chip_frame):
        """
        Remove um email da lista.
        
        Args:
            email (str): Email a remover
            chip_frame (CTkFrame): Frame do chip a destruir
        """
        if email in self.emails:
            self.emails.remove(email)
            chip_frame.destroy()
            
            # Mostrar label de instruções se não tiver mais emails
            if len(self.emails) == 0:
                self.instruction_label.pack(pady=10)
    
    def get_emails(self):
        """
        Retorna a lista de emails.
        
        Returns:
            list: Lista de endereços de email
        """
        return self.emails.copy()
    
    def set_emails(self, emails):
        """
        Define a lista de emails (substitui a atual).
        
        Args:
            emails (list): Lista de emails
        """
        # Limpar lista atual
        self.clear()
        
        # Adicionar novos emails
        for email in emails:
            self.add_email(email)
    
    def clear(self):
        """Limpa todos os emails"""
        self.emails.clear()
        
        # Destruir todos os chips
        for widget in self.chips_frame.winfo_children():
            if widget != self.instruction_label:
                widget.destroy()
        
        # Mostrar label de instruções
        if not self.instruction_label.winfo_exists():
            self.instruction_label = ctk.CTkLabel(
                self.chips_frame,
                text="Nenhum email adicionado",
                text_color="gray"
            )
        self.instruction_label.pack(pady=10)
    
    def has_emails(self):
        """
        Verifica se há emails na lista.
        
        Returns:
            bool: True se há pelo menos um email
        """
        return len(self.emails) > 0

