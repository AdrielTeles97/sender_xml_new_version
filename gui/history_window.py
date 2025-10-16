#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import customtkinter as ctk
from tkinter import Toplevel, messagebox, Frame
import logging
from datetime import datetime, timedelta

class HistoryWindow:
    """Janela de visualização do histórico de envios"""
    
    def __init__(self, parent, history_manager):
        """
        Inicializa a janela de histórico.
        
        Args:
            parent (CTk): Janela pai
            history_manager (HistoryManager): Gerenciador de histórico
        """
        self.parent = parent
        self.history_manager = history_manager
        self.logger = logging.getLogger("XMLSender.HistoryWindow")
        
        # Criar janela
        self.window = Toplevel(parent)
        self.window.title("Histórico de Envios")
        self.window.geometry("1000x700")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar a janela
        x = parent.winfo_x() + (parent.winfo_width() / 2) - (1000 / 2)
        y = parent.winfo_y() + (parent.winfo_height() / 2) - (700 / 2)
        self.window.geometry("+%d+%d" % (x, y))
        
        # Construir interface
        self._build_interface()
        
        # Carregar dados
        self._load_history()
        self._load_statistics()
    
    def _build_interface(self):
        """Constrói a interface da janela"""
        # Container principal
        main_container = Frame(self.window)
        main_container.pack(fill="both", expand=True)
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(main_container)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="📊 Histórico de Envios",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame de estatísticas
        stats_frame = ctk.CTkFrame(self.main_frame)
        stats_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.stats_labels = {}
        stats_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_container.pack(fill="x", pady=10)
        
        # Estatísticas em cards
        stat_names = [
            ("total", "Total de Envios", "🔢"),
            ("sucesso", "Bem-sucedidos", "✅"),
            ("erro", "Com Erro", "❌"),
            ("taxa", "Taxa de Sucesso", "📈"),
            ("arquivos", "Arquivos Enviados", "📦")
        ]
        
        for i, (key, label, icon) in enumerate(stat_names):
            stat_card = ctk.CTkFrame(stats_container)
            stat_card.grid(row=0, column=i, padx=5, sticky="ew")
            
            icon_label = ctk.CTkLabel(stat_card, text=icon, font=("Helvetica", 24))
            icon_label.pack(pady=(10, 0))
            
            value_label = ctk.CTkLabel(
                stat_card,
                text="0",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            value_label.pack()
            self.stats_labels[key] = value_label
            
            desc_label = ctk.CTkLabel(
                stat_card,
                text=label,
                font=("Helvetica", 10),
                text_color="gray"
            )
            desc_label.pack(pady=(0, 10))
        
        # Configurar grid
        for i in range(len(stat_names)):
            stats_container.grid_columnconfigure(i, weight=1)
        
        # Frame de filtros
        filter_frame = ctk.CTkFrame(self.main_frame)
        filter_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        filter_title = ctk.CTkLabel(
            filter_frame,
            text="🔍 Filtros:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        filter_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        filter_controls = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_controls.pack(fill="x", padx=10, pady=(0, 10))
        
        # Filtro por status
        status_label = ctk.CTkLabel(filter_controls, text="Status:")
        status_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.status_filter = ctk.CTkComboBox(
            filter_controls,
            values=["Todos", "Sucesso", "Erro", "Parcial"],
            width=120,
            command=self._on_filter_changed
        )
        self.status_filter.set("Todos")
        self.status_filter.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Filtro por documento
        doc_label = ctk.CTkLabel(filter_controls, text="Documento:")
        doc_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        
        self.doc_filter = ctk.CTkEntry(filter_controls, width=150, placeholder_text="CPF/CNPJ")
        self.doc_filter.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.doc_filter.bind("<KeyRelease>", lambda e: self._on_filter_changed())
        
        # Filtro por período
        period_label = ctk.CTkLabel(filter_controls, text="Período:")
        period_label.grid(row=0, column=4, padx=5, pady=5, sticky="e")
        
        self.period_filter = ctk.CTkComboBox(
            filter_controls,
            values=["Todos", "Hoje", "Últimos 7 dias", "Últimos 30 dias", "Últimos 90 dias"],
            width=150,
            command=self._on_filter_changed
        )
        self.period_filter.set("Últimos 30 dias")
        self.period_filter.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        
        # Botão atualizar
        refresh_button = ctk.CTkButton(
            filter_controls,
            text="🔄 Atualizar",
            width=100,
            command=self._load_history
        )
        refresh_button.grid(row=0, column=6, padx=10, pady=5)
        
        # Frame da tabela
        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Cabeçalho da tabela
        header_frame = ctk.CTkFrame(table_frame, fg_color=("#3B8ED0", "#1F6AA5"))
        header_frame.pack(fill="x", padx=2, pady=2)
        
        headers = [
            ("Data/Hora", 0.15),
            ("Documento", 0.12),
            ("Empresa", 0.18),
            ("Período", 0.08),
            ("Destinatários", 0.20),
            ("Arquivos", 0.08),
            ("Status", 0.10),
            ("Tentativas", 0.09)
        ]
        
        for i, (header, width) in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(weight="bold"),
                text_color="white"
            )
            label.place(relx=sum([h[1] for h in headers[:i]]), rely=0.5, anchor="w", 
                       relwidth=width)
        
        # Frame rolável para os dados
        self.data_frame = ctk.CTkScrollableFrame(table_frame, fg_color="transparent")
        self.data_frame.pack(fill="both", expand=True, padx=2, pady=(0, 2))
        
        # Frame de botões
        button_frame = ctk.CTkFrame(main_container)
        button_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        
        export_button = ctk.CTkButton(
            button_frame,
            text="📄 Exportar",
            command=self._export_history,
            width=100
        )
        export_button.pack(side="left", padx=10)
        
        clean_button = ctk.CTkButton(
            button_frame,
            text="🧹 Limpar Antigos",
            command=self._clean_old_records,
            width=120,
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        clean_button.pack(side="left", padx=10)
        
        close_button = ctk.CTkButton(
            button_frame,
            text="Fechar",
            command=self.window.destroy,
            width=100
        )
        close_button.pack(side="right", padx=10)
    
    def _load_statistics(self):
        """Carrega as estatísticas"""
        try:
            stats = self.history_manager.get_estatisticas()
            
            self.stats_labels['total'].configure(text=str(stats.get('total_envios', 0)))
            self.stats_labels['sucesso'].configure(text=str(stats.get('envios_sucesso', 0)))
            self.stats_labels['erro'].configure(text=str(stats.get('envios_erro', 0)))
            self.stats_labels['taxa'].configure(text=f"{stats.get('taxa_sucesso', 0):.1f}%")
            self.stats_labels['arquivos'].configure(text=str(stats.get('total_arquivos', 0)))
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar estatísticas: {e}")
    
    def _on_filter_changed(self, value=None):
        """Callback quando os filtros mudam"""
        self._load_history()
    
    def _load_history(self):
        """Carrega o histórico com base nos filtros"""
        try:
            # Limpar dados atuais
            for widget in self.data_frame.winfo_children():
                widget.destroy()
            
            # Obter valores dos filtros
            status_filter = self.status_filter.get()
            doc_filter = self.doc_filter.get().strip()
            period_filter = self.period_filter.get()
            
            # Converter filtros para parâmetros
            filtro_status = None
            if status_filter != "Todos":
                filtro_status = status_filter.lower()
            
            filtro_doc = doc_filter if doc_filter else None
            
            # Calcular datas baseado no período
            data_inicio = None
            data_fim = None
            
            if period_filter == "Hoje":
                data_inicio = datetime.now().strftime('%Y-%m-%d')
                data_fim = datetime.now().strftime('%Y-%m-%d')
            elif period_filter == "Últimos 7 dias":
                data_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            elif period_filter == "Últimos 30 dias":
                data_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            elif period_filter == "Últimos 90 dias":
                data_inicio = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            
            # Carregar histórico
            historico = self.history_manager.get_historico(
                limite=200,
                filtro_status=filtro_status,
                filtro_documento=filtro_doc,
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            
            # Exibir dados
            if not historico:
                no_data_label = ctk.CTkLabel(
                    self.data_frame,
                    text="Nenhum registro encontrado",
                    text_color="gray"
                )
                no_data_label.pack(pady=20)
                return
            
            headers = [
                ("Data/Hora", 0.15),
                ("Documento", 0.12),
                ("Empresa", 0.18),
                ("Período", 0.08),
                ("Destinatários", 0.20),
                ("Arquivos", 0.08),
                ("Status", 0.10),
                ("Tentativas", 0.09)
            ]
            
            for record in historico:
                row_frame = ctk.CTkFrame(
                    self.data_frame,
                    fg_color=("#E8E8E8", "#2B2B2B"),
                    height=40
                )
                row_frame.pack(fill="x", padx=2, pady=2)
                row_frame.pack_propagate(False)
                
                # Formatar data
                data_envio = record['data_envio'].split('.')[0] if '.' in record['data_envio'] else record['data_envio']
                
                # Truncar destinatários se muito longo
                dest = record['destinatarios']
                if len(dest) > 30:
                    dest = dest[:27] + "..."
                
                # Cor do status
                status = record['status']
                if status == 'sucesso':
                    status_color = "#4CAF50"
                    status_text = "✓ Sucesso"
                elif status == 'erro':
                    status_color = "#F44336"
                    status_text = "✗ Erro"
                else:
                    status_color = "#FF9800"
                    status_text = "⚠ Parcial"
                
                values = [
                    data_envio,
                    record['documento'],
                    record['empresa'][:20] if len(record['empresa']) > 20 else record['empresa'],
                    record['periodo'],
                    dest,
                    f"{record['total_arquivos']} ({record['nfce_count']}+{record['nfe_count']})",
                    status_text,
                    str(record['tentativas'])
                ]
                
                for i, (value, (header, width)) in enumerate(zip(values, headers)):
                    label = ctk.CTkLabel(
                        row_frame,
                        text=value,
                        font=("Helvetica", 10),
                        text_color=status_color if i == 6 else None
                    )
                    label.place(relx=sum([h[1] for h in headers[:i]]), rely=0.5, anchor="w",
                               relwidth=width)
                
                # Adicionar tooltip com erro se houver
                if record['erro']:
                    row_frame.bind("<Button-1>", 
                                  lambda e, err=record['erro']: messagebox.showinfo(
                                      "Detalhes do Erro", err))
            
            # Atualizar estatísticas
            self._load_statistics()
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar histórico: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar histórico: {e}")
    
    def _export_history(self):
        """Exporta o histórico para CSV"""
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de exportação em desenvolvimento")
    
    def _clean_old_records(self):
        """Limpa registros antigos"""
        result = messagebox.askyesno(
            "Confirmar Limpeza",
            "Deseja remover registros com mais de 90 dias?\n\nEsta ação não pode ser desfeita."
        )
        
        if result:
            try:
                deleted = self.history_manager.limpar_historico_antigo(90)
                messagebox.showinfo("Sucesso", f"{deleted} registro(s) removido(s).")
                self._load_history()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar registros: {e}")

