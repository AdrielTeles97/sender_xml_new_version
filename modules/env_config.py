#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging

class EnvConfig:
    """Gerenciador de variáveis de ambiente"""
    
    def __init__(self, env_file=".env"):
        """
        Inicializa o gerenciador de variáveis de ambiente.
        
        Args:
            env_file (str): Caminho para o arquivo .env
        """
        self.logger = logging.getLogger("XMLSender.EnvConfig")
        self.env_file = env_file
        self.config = {}
        self._load_env()
    
    def _load_env(self):
        """Carrega variáveis do arquivo .env"""
        if not os.path.exists(self.env_file):
            self.logger.warning(f"Arquivo {self.env_file} não encontrado. Usando valores padrão.")
            return
        
        try:
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Ignorar linhas vazias e comentários
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parsear linha no formato KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remover aspas se houver
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        self.config[key] = value
            
            self.logger.info(f"Variáveis de ambiente carregadas de {self.env_file}")
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar {self.env_file}: {e}")
    
    def get(self, key, default=None):
        """
        Obtém valor de uma variável de ambiente.
        
        Args:
            key (str): Nome da variável
            default: Valor padrão se não encontrada
            
        Returns:
            str: Valor da variável
        """
        # Primeiro tenta do arquivo .env
        value = self.config.get(key)
        
        # Se não encontrou, tenta das variáveis de ambiente do sistema
        if value is None:
            value = os.environ.get(key)
        
        # Se ainda não encontrou, retorna o padrão
        if value is None:
            value = default
        
        return value
    
    def get_smtp_config(self):
        """
        Retorna configuração SMTP a partir do .env
        
        Returns:
            dict: Configuração SMTP
        """
        smtp_config = {
            'server': self.get('SMTP_SERVER', 'smtp.gmail.com'),
            'port': int(self.get('SMTP_PORT', '587')),
            'username': self.get('SMTP_USERNAME', ''),
            'password': self.get('SMTP_PASSWORD', ''),
            'use_ssl': self.get('SMTP_USE_SSL', 'false').lower() == 'true'
        }
        
        # Validar se as credenciais estão preenchidas
        if not smtp_config['username'] or not smtp_config['password']:
            self.logger.warning("Credenciais SMTP não configuradas no .env")
        
        return smtp_config

