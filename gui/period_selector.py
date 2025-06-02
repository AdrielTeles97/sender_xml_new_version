#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import customtkinter as ctk
from datetime import datetime, timedelta
import calendar

class PeriodSelector(ctk.CTkFrame):
    """Componente para seleção de períodos no formato YYYY-MM"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.periods = []
        
        # Frame para o título e botão de adicionar
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Label para o título
        self.title_label = ctk.CTkLabel(self.header_frame, text="Períodos selecionados:", anchor="w")
        self.title_label.pack(side="left", padx=5)
        
        # Botão para adicionar novo período
        self.add_btn = ctk.CTkButton(self.header_frame, text="+", width=30, 
                                     command=self.add_period)
        self.add_btn.pack(side="right", padx=5)
        
        # Frame para a lista de períodos com espaçamento adequado
        self.periods_frame = ctk.CTkScrollableFrame(self, height=150)
        self.periods_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Inicializa com o mês anterior
        self.add_period()
    
    def get_year_range(self):
        """
        Retorna um intervalo dinâmico de anos: 10 anos atrás e 10 anos à frente
        do ano atual.
        """
        current_year = datetime.now().year
        return list(range(current_year - 10, current_year + 11))
    
    def add_period(self):
        """Adiciona um novo seletor de período"""
        # Obter mês anterior como padrão
        today = datetime.now()
        last_month = today.replace(day=1) - timedelta(days=1)
        default_year = last_month.year
        default_month = last_month.month
        
        # Criar frame para este período com margem para separação visual
        period_frame = ctk.CTkFrame(self.periods_frame, fg_color=("#E5E5E5", "#333333"))
        period_frame.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5)
        
        # Criar frame interno para organizar os elementos
        content_frame = ctk.CTkFrame(period_frame)
        content_frame.pack(fill="x", expand=True, padx=5, pady=5)
        
        # Frame para as labels descritivas
        label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        label_frame.pack(fill="x", pady=(0, 2))
        
        # Label para ano
        year_label = ctk.CTkLabel(label_frame, text="Ano:", font=("Helvetica", 11), anchor="w")
        year_label.pack(side="left", padx=(5, 2))
        
        # Espaçador
        spacer = ctk.CTkLabel(label_frame, text="", width=30)
        spacer.pack(side="left")
        
        # Label para mês
        month_label = ctk.CTkLabel(label_frame, text="Mês:", font=("Helvetica", 11), anchor="w")
        month_label.pack(side="left", padx=(30, 2))
        
        # Frame para os seletores
        selectors_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        selectors_frame.pack(fill="x")
        
        # Gerar intervalo dinâmico de anos (10 anos atrás e 10 anos à frente)
        years = self.get_year_range()
        
        # Dropdown para ano
        year_var = ctk.StringVar(value=str(default_year))
        year_dropdown = ctk.CTkComboBox(
            selectors_frame,
            values=[str(y) for y in years],
            variable=year_var,
            width=80,
        )
        year_dropdown.pack(side="left", padx=(5, 2))
        
        # Separador
        separator = ctk.CTkLabel(selectors_frame, text="-", width=10)
        separator.pack(side="left", padx=0)
        
        # Dropdown para mês
        months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        month_names = {
            "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
            "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
            "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
        }
        
        month_options = []
        for m in months:
            month_option = f"{m} ({month_names[m][:3]})"  # Abreviando para os primeiros 3 caracteres
            month_options.append(month_option)
        
        month_var = ctk.StringVar(value=month_options[default_month-1])
        month_dropdown = ctk.CTkComboBox(
            selectors_frame,
            values=month_options,
            variable=month_var,
            width=120,
        )
        month_dropdown.pack(side="left", padx=(2, 5))
        
        # Criar um ID único para este período
        period_id = len(self.periods)
        
        # Botão para remover este período
        remove_btn = ctk.CTkButton(
            selectors_frame, 
            text="✕", 
            width=30, 
            fg_color="#D32F2F",  
            hover_color="#B71C1C",
            command=lambda id=period_id: self._remove_period_by_id(id)
        )
        remove_btn.pack(side="right", padx=5)
        
        # Armazenar dados deste período para recuperação posterior
        period_data = {
            "id": period_id,
            "frame": period_frame,
            "year_var": year_var,
            "month_var": month_var,
            "year_dropdown": year_dropdown,
            "month_dropdown": month_dropdown,
            "remove_button": remove_btn
        }
        
        self.periods.append(period_data)
        
        # Atualizar a visibilidade dos botões de remoção
        self.update_remove_buttons()
        
    def update_remove_buttons(self):
        """Atualiza a visibilidade dos botões de remoção com base no número de períodos"""
        # Se houver apenas um período, desativar o botão de remoção
        if len(self.periods) <= 1:
            for period in self.periods:
                period["remove_button"].configure(state="disabled")
        else:
            # Se houver mais de um período, ativar todos os botões de remoção
            for period in self.periods:
                period["remove_button"].configure(state="normal")
    
    def _remove_period_by_id(self, period_id):
        """
        Remove um período específico pelo seu ID.
        
        Args:
            period_id (int): ID do período a ser removido
        """
        if len(self.periods) <= 1:
            return  # Não remover se for o último período
        
        # Encontrar o período pelo ID
        for i, period in enumerate(self.periods):
            if period["id"] == period_id:
                # Remover da interface
                period["frame"].destroy()
                # Remover da lista
                self.periods.pop(i)
                # Atualizar botões
                self.update_remove_buttons()
                return
    
    def remove_period(self, period_frame):
        """Método legado, mantido para compatibilidade"""
        for i, period in enumerate(self.periods):
            if period["frame"] == period_frame:
                self._remove_period_by_id(period["id"])
                return
    
    def get_periods(self):
        """Retorna todos os períodos selecionados no formato YYYY-MM"""
        periods = []
        for period_data in self.periods:
            year = period_data["year_var"].get()
            # Extrai apenas o número do mês (primeiros 2 caracteres)
            month = period_data["month_var"].get().split()[0]
            period = f"{year}-{month}"
            periods.append(period)
        return periods
    
    def get_formatted_periods(self):
        """Retorna os períodos em formato legível (para exibição)"""
        formatted_periods = []
        month_names = {
            "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
            "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
            "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
        }
        
        for period_data in self.periods:
            year = period_data["year_var"].get()
            month_code = period_data["month_var"].get().split()[0]
            month_name = month_names.get(month_code, month_code)
            formatted_periods.append(f"{month_name} de {year}")
        
        return formatted_periods