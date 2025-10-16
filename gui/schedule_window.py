#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import customtkinter as ctk
from tkinter import Toplevel, messagebox, Frame
from datetime import datetime, timedelta
import logging

class ScheduleWindow:
    """Janela para criar e gerenciar agendamentos"""
    
    def __init__(self, parent, history_manager, config):
        """
        Inicializa a janela de agendamento.
        
        Args:
            parent (CTk): Janela pai
            history_manager (HistoryManager): Gerenciador de histórico
            config (dict): Configurações da aplicação
        """
        self.parent = parent
        self.history_manager = history_manager
        self.config = config
        self.logger = logging.getLogger("XMLSender.ScheduleWindow")
        
        # Criar janela
        self.window = Toplevel(parent)
        self.window.title("Agendamento de Envios")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar
        x = parent.winfo_x() + (parent.winfo_width() / 2) - (600 / 2)
        y = parent.winfo_y() + (parent.winfo_height() / 2) - (500 / 2)
        self.window.geometry("+%d+%d" % (x, y))
        
        # Construir interface
        self._build_interface()
    
    def _build_interface(self):
        """Constrói a interface"""
        main_container = Frame(self.window)
        main_container.pack(fill="both", expand=True)
        
        main_frame = ctk.CTkFrame(main_container)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="📅 Agendar Envio Automático",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=10)
        
        # Frame do formulário
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Data e Hora
        datetime_label = ctk.CTkLabel(form_frame, text="Data e Hora:", font=("Helvetica", 12, "bold"))
        datetime_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        datetime_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        datetime_container.pack(fill="x", padx=10)
        
        # Data
        date_frame = ctk.CTkFrame(datetime_container, fg_color="transparent")
        date_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(date_frame, text="Data:").pack(anchor="w")
        date_sub = ctk.CTkFrame(date_frame, fg_color="transparent")
        date_sub.pack(fill="x")
        
        tomorrow = datetime.now() + timedelta(days=1)
        
        self.day_var = ctk.StringVar(value=str(tomorrow.day))
        day_entry = ctk.CTkEntry(date_sub, textvariable=self.day_var, width=50)
        day_entry.pack(side="left", padx=2)
        ctk.CTkLabel(date_sub, text="/").pack(side="left")
        
        self.month_var = ctk.StringVar(value=str(tomorrow.month))
        month_entry = ctk.CTkEntry(date_sub, textvariable=self.month_var, width=50)
        month_entry.pack(side="left", padx=2)
        ctk.CTkLabel(date_sub, text="/").pack(side="left")
        
        self.year_var = ctk.StringVar(value=str(tomorrow.year))
        year_entry = ctk.CTkEntry(date_sub, textvariable=self.year_var, width=70)
        year_entry.pack(side="left", padx=2)
        
        # Hora
        time_frame = ctk.CTkFrame(datetime_container, fg_color="transparent")
        time_frame.pack(side="left", fill="x", expand=True, padx=(20, 0))
        
        ctk.CTkLabel(time_frame, text="Hora:").pack(anchor="w")
        time_sub = ctk.CTkFrame(time_frame, fg_color="transparent")
        time_sub.pack(fill="x")
        
        self.hour_var = ctk.StringVar(value="08")
        hour_entry = ctk.CTkEntry(time_sub, textvariable=self.hour_var, width=50)
        hour_entry.pack(side="left", padx=2)
        ctk.CTkLabel(time_sub, text=":").pack(side="left")
        
        self.minute_var = ctk.StringVar(value="00")
        minute_entry = ctk.CTkEntry(time_sub, textvariable=self.minute_var, width=50)
        minute_entry.pack(side="left", padx=2)
        
        # Recorrência
        recurrence_label = ctk.CTkLabel(form_frame, text="Recorrência:", font=("Helvetica", 12, "bold"))
        recurrence_label.pack(anchor="w", padx=10, pady=(15, 5))
        
        self.recurrent_var = ctk.BooleanVar(value=False)
        recurrent_check = ctk.CTkCheckBox(
            form_frame,
            text="Envio recorrente",
            variable=self.recurrent_var,
            command=self._toggle_recurrence
        )
        recurrent_check.pack(anchor="w", padx=10)
        
        self.recurrence_type = ctk.CTkComboBox(
            form_frame,
            values=["Diariamente", "Semanalmente", "Mensalmente"],
            state="disabled",
            width=200
        )
        self.recurrence_type.pack(anchor="w", padx=10, pady=5)
        
        # Observações
        obs_label = ctk.CTkLabel(form_frame, text="Observações:", font=("Helvetica", 12, "bold"))
        obs_label.pack(anchor="w", padx=10, pady=(15, 5))
        
        self.obs_text = ctk.CTkTextbox(form_frame, height=80)
        self.obs_text.pack(fill="x", padx=10, pady=5)
        
        # Informação
        info_frame = ctk.CTkFrame(form_frame, fg_color=("#E3F2FD", "#1565C0"))
        info_frame.pack(fill="x", padx=10, pady=10)
        
        info_text = (
            "ℹ️ O agendamento usará os dados do formulário principal:\n"
            "• Documento, Empresa e Emails configurados\n"
            "• Períodos selecionados no momento do envio"
        )
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            justify="left",
            font=("Helvetica", 10)
        )
        info_label.pack(padx=10, pady=10)
        
        # Botões
        button_frame = ctk.CTkFrame(main_container)
        button_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        
        save_button = ctk.CTkButton(
            button_frame,
            text="✓ Agendar",
            command=self._save_schedule,
            width=120
        )
        save_button.pack(side="left", padx=10)
        
        view_button = ctk.CTkButton(
            button_frame,
            text="📋 Ver Agendamentos",
            command=self._view_schedules,
            width=150
        )
        view_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self.window.destroy,
            width=100
        )
        cancel_button.pack(side="right", padx=10)
    
    def _toggle_recurrence(self):
        """Alterna o estado do campo de recorrência"""
        if self.recurrent_var.get():
            self.recurrence_type.configure(state="normal")
        else:
            self.recurrence_type.configure(state="disabled")
    
    def _save_schedule(self):
        """Salva o agendamento"""
        try:
            # Validar campos
            day = int(self.day_var.get())
            month = int(self.month_var.get())
            year = int(self.year_var.get())
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            
            # Criar data/hora
            scheduled_datetime = datetime(year, month, day, hour, minute)
            
            # Verificar se é data futura
            if scheduled_datetime <= datetime.now():
                messagebox.showerror("Erro", "A data agendada deve ser futura!")
                return
            
            # Obter dados da configuração
            documento = self.config.get('document_id_clean', '')
            empresa = self.config.get('company_name', '')
            email = self.config.get('email', '')
            
            if not documento or not empresa or not email:
                messagebox.showerror(
                    "Erro",
                    "Preencha os campos Documento, Empresa e Email no formulário principal antes de agendar."
                )
                return
            
            # Criar agendamento
            recorrente = self.recurrent_var.get()
            recorrencia_tipo = None
            if recorrente:
                tipo_map = {
                    "Diariamente": "diaria",
                    "Semanalmente": "semanal",
                    "Mensalmente": "mensal"
                }
                recorrencia_tipo = tipo_map.get(self.recurrence_type.get())
            
            observacoes = self.obs_text.get("1.0", "end-1c").strip()
            
            agendamento_id = self.history_manager.add_agendamento(
                data_agendada=scheduled_datetime,
                documento=documento,
                empresa=empresa,
                periodos=["auto"],  # Será determinado no momento da execução
                destinatarios=[email],
                recorrente=recorrente,
                recorrencia_tipo=recorrencia_tipo,
                observacoes=observacoes
            )
            
            if agendamento_id:
                messagebox.showinfo(
                    "Sucesso",
                    f"Agendamento criado com sucesso!\n\n"
                    f"Data: {scheduled_datetime.strftime('%d/%m/%Y %H:%M')}\n"
                    f"Recorrente: {'Sim' if recorrente else 'Não'}"
                )
                self.window.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao criar agendamento.")
            
        except ValueError as e:
            messagebox.showerror("Erro", "Data/hora inválida. Verifique os valores informados.")
        except Exception as e:
            self.logger.error(f"Erro ao salvar agendamento: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar agendamento: {e}")
    
    def _view_schedules(self):
        """Abre janela para visualizar agendamentos"""
        messagebox.showinfo("Em Desenvolvimento", "Visualização de agendamentos em desenvolvimento")

