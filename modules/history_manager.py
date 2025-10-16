#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import logging
from datetime import datetime
import json

class HistoryManager:
    """Gerenciador de histórico de envios"""
    
    def __init__(self, db_path='data/history.db'):
        """
        Inicializa o gerenciador de histórico.
        
        Args:
            db_path (str): Caminho para o banco de dados SQLite
        """
        self.db_path = db_path
        self.logger = logging.getLogger("XMLSender.HistoryManager")
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Inicializar banco de dados
        self._init_database()
    
    def _init_database(self):
        """Cria as tabelas do banco de dados se não existirem"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabela de envios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS envios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    documento TEXT NOT NULL,
                    empresa TEXT NOT NULL,
                    periodo TEXT NOT NULL,
                    destinatarios TEXT NOT NULL,
                    total_arquivos INTEGER DEFAULT 0,
                    nfce_count INTEGER DEFAULT 0,
                    nfe_count INTEGER DEFAULT 0,
                    status TEXT NOT NULL,
                    tentativas INTEGER DEFAULT 1,
                    erro TEXT,
                    arquivo_zip TEXT,
                    tempo_processamento REAL,
                    observacoes TEXT
                )
            ''')
            
            # Tabela de agendamentos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agendamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_agendada TIMESTAMP NOT NULL,
                    documento TEXT NOT NULL,
                    empresa TEXT NOT NULL,
                    periodos TEXT NOT NULL,
                    destinatarios TEXT NOT NULL,
                    status TEXT DEFAULT 'pendente',
                    executado_em TIMESTAMP,
                    recorrente BOOLEAN DEFAULT 0,
                    recorrencia_tipo TEXT,
                    ativo BOOLEAN DEFAULT 1,
                    observacoes TEXT
                )
            ''')
            
            # Índices para melhor performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_envios_data ON envios(data_envio)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_envios_status ON envios(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_envios_documento ON envios(documento)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_agendamentos_data ON agendamentos(data_agendada)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_agendamentos_status ON agendamentos(status)')
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Banco de dados inicializado: {self.db_path}")
            
        except Exception as e:
            self.logger.error(f"Erro ao inicializar banco de dados: {e}")
            raise
    
    def add_envio(self, documento, empresa, periodo, destinatarios, 
                  nfce_count=0, nfe_count=0, status='sucesso', 
                  tentativas=1, erro=None, arquivo_zip=None,
                  tempo_processamento=None, observacoes=None):
        """
        Adiciona um registro de envio ao histórico.
        
        Args:
            documento (str): CPF/CNPJ
            empresa (str): Nome da empresa
            periodo (str): Período no formato YYYY-MM
            destinatarios (list ou str): Lista de emails ou email único
            nfce_count (int): Quantidade de NFCe
            nfe_count (int): Quantidade de NFe
            status (str): Status do envio ('sucesso', 'erro', 'parcial')
            tentativas (int): Número de tentativas realizadas
            erro (str): Mensagem de erro, se houver
            arquivo_zip (str): Caminho do arquivo ZIP gerado
            tempo_processamento (float): Tempo de processamento em segundos
            observacoes (str): Observações adicionais
            
        Returns:
            int: ID do registro inserido
        """
        try:
            # Converter lista de destinatários para string
            if isinstance(destinatarios, list):
                destinatarios_str = '; '.join(destinatarios)
            else:
                destinatarios_str = destinatarios
            
            total_arquivos = nfce_count + nfe_count
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO envios 
                (documento, empresa, periodo, destinatarios, total_arquivos, 
                 nfce_count, nfe_count, status, tentativas, erro, arquivo_zip,
                 tempo_processamento, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (documento, empresa, periodo, destinatarios_str, total_arquivos,
                  nfce_count, nfe_count, status, tentativas, erro, arquivo_zip,
                  tempo_processamento, observacoes))
            
            envio_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.logger.info(f"Envio registrado no histórico: ID {envio_id}")
            return envio_id
            
        except Exception as e:
            self.logger.error(f"Erro ao adicionar envio ao histórico: {e}")
            return None
    
    def get_historico(self, limite=100, filtro_status=None, filtro_documento=None, 
                      data_inicio=None, data_fim=None):
        """
        Recupera o histórico de envios com filtros opcionais.
        
        Args:
            limite (int): Número máximo de registros
            filtro_status (str): Filtrar por status
            filtro_documento (str): Filtrar por documento
            data_inicio (str): Data inicial (formato: YYYY-MM-DD)
            data_fim (str): Data final (formato: YYYY-MM-DD)
            
        Returns:
            list: Lista de dicionários com os registros
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
            cursor = conn.cursor()
            
            # Construir query dinâmica
            query = "SELECT * FROM envios WHERE 1=1"
            params = []
            
            if filtro_status:
                query += " AND status = ?"
                params.append(filtro_status)
            
            if filtro_documento:
                query += " AND documento LIKE ?"
                params.append(f"%{filtro_documento}%")
            
            if data_inicio:
                query += " AND DATE(data_envio) >= ?"
                params.append(data_inicio)
            
            if data_fim:
                query += " AND DATE(data_envio) <= ?"
                params.append(data_fim)
            
            query += " ORDER BY data_envio DESC LIMIT ?"
            params.append(limite)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Converter para lista de dicionários
            historico = []
            for row in rows:
                historico.append({
                    'id': row['id'],
                    'data_envio': row['data_envio'],
                    'documento': row['documento'],
                    'empresa': row['empresa'],
                    'periodo': row['periodo'],
                    'destinatarios': row['destinatarios'],
                    'total_arquivos': row['total_arquivos'],
                    'nfce_count': row['nfce_count'],
                    'nfe_count': row['nfe_count'],
                    'status': row['status'],
                    'tentativas': row['tentativas'],
                    'erro': row['erro'],
                    'arquivo_zip': row['arquivo_zip'],
                    'tempo_processamento': row['tempo_processamento'],
                    'observacoes': row['observacoes']
                })
            
            conn.close()
            return historico
            
        except Exception as e:
            self.logger.error(f"Erro ao recuperar histórico: {e}")
            return []
    
    def get_estatisticas(self):
        """
        Retorna estatísticas do histórico.
        
        Returns:
            dict: Dicionário com estatísticas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de envios
            cursor.execute("SELECT COUNT(*) FROM envios")
            total_envios = cursor.fetchone()[0]
            
            # Envios bem-sucedidos
            cursor.execute("SELECT COUNT(*) FROM envios WHERE status = 'sucesso'")
            envios_sucesso = cursor.fetchone()[0]
            
            # Envios com erro
            cursor.execute("SELECT COUNT(*) FROM envios WHERE status = 'erro'")
            envios_erro = cursor.fetchone()[0]
            
            # Total de arquivos enviados
            cursor.execute("SELECT SUM(total_arquivos) FROM envios WHERE status = 'sucesso'")
            total_arquivos = cursor.fetchone()[0] or 0
            
            # Último envio
            cursor.execute("SELECT data_envio FROM envios ORDER BY data_envio DESC LIMIT 1")
            ultimo_envio = cursor.fetchone()
            ultimo_envio = ultimo_envio[0] if ultimo_envio else None
            
            conn.close()
            
            return {
                'total_envios': total_envios,
                'envios_sucesso': envios_sucesso,
                'envios_erro': envios_erro,
                'taxa_sucesso': (envios_sucesso / total_envios * 100) if total_envios > 0 else 0,
                'total_arquivos': total_arquivos,
                'ultimo_envio': ultimo_envio
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def add_agendamento(self, data_agendada, documento, empresa, periodos,
                        destinatarios, recorrente=False, recorrencia_tipo=None,
                        observacoes=None):
        """
        Adiciona um agendamento de envio.
        
        Args:
            data_agendada (datetime ou str): Data/hora agendada
            documento (str): CPF/CNPJ
            empresa (str): Nome da empresa
            periodos (list): Lista de períodos
            destinatarios (list): Lista de emails
            recorrente (bool): Se é recorrente
            recorrencia_tipo (str): Tipo de recorrência ('diaria', 'semanal', 'mensal')
            observacoes (str): Observações
            
        Returns:
            int: ID do agendamento
        """
        try:
            # Converter data para string se necessário
            if isinstance(data_agendada, datetime):
                data_agendada_str = data_agendada.strftime('%Y-%m-%d %H:%M:%S')
            else:
                data_agendada_str = data_agendada
            
            # Converter listas para JSON
            periodos_json = json.dumps(periodos) if isinstance(periodos, list) else periodos
            destinatarios_json = json.dumps(destinatarios) if isinstance(destinatarios, list) else destinatarios
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO agendamentos
                (data_agendada, documento, empresa, periodos, destinatarios,
                 recorrente, recorrencia_tipo, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data_agendada_str, documento, empresa, periodos_json,
                  destinatarios_json, recorrente, recorrencia_tipo, observacoes))
            
            agendamento_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.logger.info(f"Agendamento criado: ID {agendamento_id}")
            return agendamento_id
            
        except Exception as e:
            self.logger.error(f"Erro ao criar agendamento: {e}")
            return None
    
    def get_agendamentos_pendentes(self):
        """
        Retorna agendamentos pendentes que devem ser executados.
        
        Returns:
            list: Lista de agendamentos pendentes
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM agendamentos
                WHERE status = 'pendente'
                AND ativo = 1
                AND datetime(data_agendada) <= datetime('now')
                ORDER BY data_agendada
            ''')
            
            rows = cursor.fetchall()
            
            agendamentos = []
            for row in rows:
                agendamentos.append({
                    'id': row['id'],
                    'data_agendada': row['data_agendada'],
                    'documento': row['documento'],
                    'empresa': row['empresa'],
                    'periodos': json.loads(row['periodos']),
                    'destinatarios': json.loads(row['destinatarios']),
                    'recorrente': bool(row['recorrente']),
                    'recorrencia_tipo': row['recorrencia_tipo'],
                    'observacoes': row['observacoes']
                })
            
            conn.close()
            return agendamentos
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar agendamentos pendentes: {e}")
            return []
    
    def marcar_agendamento_executado(self, agendamento_id):
        """
        Marca um agendamento como executado.
        
        Args:
            agendamento_id (int): ID do agendamento
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE agendamentos
                SET status = 'executado',
                    executado_em = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (agendamento_id,))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Agendamento {agendamento_id} marcado como executado")
            
        except Exception as e:
            self.logger.error(f"Erro ao marcar agendamento como executado: {e}")
    
    def cancelar_agendamento(self, agendamento_id):
        """
        Cancela um agendamento.
        
        Args:
            agendamento_id (int): ID do agendamento
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE agendamentos
                SET ativo = 0,
                    status = 'cancelado'
                WHERE id = ?
            ''', (agendamento_id,))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Agendamento {agendamento_id} cancelado")
            
        except Exception as e:
            self.logger.error(f"Erro ao cancelar agendamento: {e}")
    
    def limpar_historico_antigo(self, dias=90):
        """
        Remove registros de histórico mais antigos que X dias.
        
        Args:
            dias (int): Número de dias para manter
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM envios
                WHERE DATE(data_envio) < DATE('now', '-' || ? || ' days')
            ''', (dias,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            self.logger.info(f"Removidos {deleted_count} registros antigos do histórico")
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Erro ao limpar histórico: {e}")
            return 0

